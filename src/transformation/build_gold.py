from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SILVER = BASE / 'data' / 'silver'
GOLD = BASE / 'data' / 'gold'


def read_csv(name: str):
    with (SILVER / f'{name}.csv').open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(name: str, rows: list[dict]):
    path = GOLD / f'{name}.csv'
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def q(value: str) -> Decimal:
    return Decimal(value)


def main():
    GOLD.mkdir(parents=True, exist_ok=True)
    (GOLD / '_metadata').mkdir(exist_ok=True)

    customers = read_csv('customers')
    products = read_csv('products')
    stores = read_csv('stores')
    promotions = read_csv('promotions')
    orders = read_csv('orders')
    items = read_csv('order_items')
    payments = read_csv('payments')
    inventory = read_csv('inventory')

    # Dimensions
    write_csv('dim_customer', [{k: v for k, v in r.items() if not k.startswith(('source_', 'silver_', 'record_', 'dq_'))} for r in customers])
    write_csv('dim_product', [{k: v for k, v in r.items() if not k.startswith(('source_', 'silver_', 'record_', 'dq_'))} for r in products])
    write_csv('dim_store', [{k: v for k, v in r.items() if not k.startswith(('source_', 'silver_', 'record_', 'dq_'))} for r in stores])
    write_csv('dim_promotion', [{k: v for k, v in r.items() if not k.startswith(('source_', 'silver_', 'record_', 'dq_'))} for r in promotions])

    # Date dimension based on order date range.
    dates = sorted({r['order_date'] for r in orders if r.get('order_date')})
    if dates:
        start, end = date.fromisoformat(dates[0]), date.fromisoformat(dates[-1])
        rows = []
        cur = start
        while cur <= end:
            rows.append({
                'date': cur.isoformat(),
                'year': cur.year,
                'month': cur.month,
                'month_name': cur.strftime('%B'),
                'quarter': f'Q{((cur.month - 1)//3)+1}',
                'week': cur.isocalendar().week,
                'day_of_week': cur.weekday() + 1,
            })
            cur += timedelta(days=1)
        write_csv('dim_date', rows)

    customer_map = {r['customer_id']: r for r in customers}
    product_map = {r['product_id']: r for r in products}
    store_map = {r['store_id']: r for r in stores}
    payment_map = defaultdict(list)
    for p in payments:
        payment_map[p['order_id']].append(p)

    # Fact order: one row per order.
    fact_order = []
    recognized_orders = 0
    recognized_revenue = Decimal('0')
    for o in orders:
        approved = any(p['payment_status'] == 'APPROVED' for p in payment_map[o['order_id']])
        recognized = q(o['total_amount']) if o['status'] == 'COMPLETED' and approved else Decimal('0')
        if recognized > 0:
            recognized_orders += 1
            recognized_revenue += recognized
        fact_order.append({
            'order_id': o['order_id'],
            'customer_id': o['customer_id'],
            'store_id': o['store_id'],
            'order_date': o['order_date'],
            'channel': o['channel'],
            'status': o['status'],
            'total_amount': o['total_amount'],
            'payment_approved': approved,
            'revenue_recognized': f'{recognized:.2f}',
        })
    write_csv('fact_order', fact_order)

    # Fact sales line: one row per order item.
    fact_sales = []
    for i in items:
        order = next((o for o in orders if o['order_id'] == i['order_id']), None)
        product = product_map[i['product_id']]
        gross = q(i['gross_amount'])
        net = q(i['net_amount'])
        recognized = net if order and order['status'] == 'COMPLETED' else Decimal('0')
        cost = q(product['unit_cost']) * int(i['quantity'])
        margin = recognized - cost
        fact_sales.append({
            'order_item_id': i['order_item_id'],
            'order_id': i['order_id'],
            'product_id': i['product_id'],
            'customer_id': order['customer_id'] if order else '',
            'store_id': order['store_id'] if order else '',
            'order_date': order['order_date'] if order else '',
            'channel': order['channel'] if order else '',
            'category': product['category'],
            'quantity': i['quantity'],
            'gross_amount': f'{gross:.2f}',
            'net_amount': f'{net:.2f}',
            'recognized_revenue': f'{recognized:.2f}',
            'cost_amount': f'{cost:.2f}',
            'gross_margin': f'{margin:.2f}',
        })
    write_csv('fact_sales_line', fact_sales)

    # Inventory snapshot: one row per product/store/date.
    inv_rows = []
    for r in inventory:
        risk = 'CRITICAL' if int(r['on_hand_qty']) <= int(r['reorder_point']) else ('LOW' if int(r['on_hand_qty']) <= int(r['reorder_point']) * 2 else 'HEALTHY')
        score = 100 if risk == 'CRITICAL' else 50 if risk == 'LOW' else 10
        inv_rows.append({**r, 'risk_score': score})
    write_csv('fact_inventory_snapshot', inv_rows)
    write_csv('mart_inventory_risk', [
        {
            **r,
            'product_name': product_map[r['product_id']]['product_name'],
            'category': product_map[r['product_id']]['category'],
            'store_name': store_map[r['store_id']]['store_name'],
        }
        for r in inv_rows
    ])

    # Marts.
    cat = defaultdict(lambda: {'revenue': Decimal('0'), 'margin': Decimal('0'), 'units': 0, 'orders': set()})
    channel = defaultdict(lambda: {'revenue': Decimal('0'), 'margin': Decimal('0'), 'units': 0, 'orders': set()})
    store = defaultdict(lambda: {'revenue': Decimal('0'), 'margin': Decimal('0'), 'units': 0, 'orders': set()})
    customer = defaultdict(lambda: {'revenue': Decimal('0'), 'orders': set(), 'last_order': ''})

    for r in fact_sales:
        revenue = q(r['recognized_revenue'])
        margin = q(r['gross_margin'])
        units = int(r['quantity'])
        cat[r['category']]['revenue'] += revenue
        cat[r['category']]['margin'] += margin
        cat[r['category']]['units'] += units
        cat[r['category']]['orders'].add(r['order_id'])
        channel[r['channel']]['revenue'] += revenue
        channel[r['channel']]['margin'] += margin
        channel[r['channel']]['units'] += units
        channel[r['channel']]['orders'].add(r['order_id'])
        if r['store_id']:
            store[r['store_id']]['revenue'] += revenue
            store[r['store_id']]['margin'] += margin
            store[r['store_id']]['units'] += units
            store[r['store_id']]['orders'].add(r['order_id'])
        if r['customer_id']:
            customer[r['customer_id']]['revenue'] += revenue
            customer[r['customer_id']]['orders'].add(r['order_id'])
            if r['order_date'] > customer[r['customer_id']]['last_order']:
                customer[r['customer_id']]['last_order'] = r['order_date']

    def mart_rows(bucket, key_name, label_fn=lambda k: k):
        out = []
        for k, v in bucket.items():
            rev = v['revenue']
            mar = v['margin']
            out.append({
                key_name: label_fn(k),
                'revenue': f'{rev:.2f}',
                'gross_margin': f'{mar:.2f}',
                'margin_pct': f'{(mar / rev * 100 if rev else 0):.2f}',
                'units': v['units'],
                'orders': len(v['orders']),
            })
        return sorted(out, key=lambda x: Decimal(x['revenue']), reverse=True)

    write_csv('mart_sales_by_category', mart_rows(cat, 'category'))
    write_csv('mart_sales_by_channel', mart_rows(channel, 'channel'))
    write_csv('mart_store_performance', mart_rows(store, 'store_id', lambda k: k))

    customer_rows = []
    for cid, v in customer.items():
        rev = v['revenue']
        customer_rows.append({
            'customer_id': cid,
            'customer_segment': customer_map[cid]['customer_segment'],
            'orders': len(v['orders']),
            'revenue': f'{rev:.2f}',
            'avg_order_value': f'{(rev / len(v["orders"]) if v["orders"] else 0):.2f}',
            'last_order_date': v['last_order'],
        })
    write_csv('mart_customer_value', sorted(customer_rows, key=lambda x: Decimal(x['revenue']), reverse=True))

    reconciliation = {
        'completed_approved_orders_source': recognized_orders,
        'orders_with_recognized_revenue_gold': sum(Decimal(r['revenue_recognized']) > 0 for r in fact_order),
        'recognized_revenue': f'{recognized_revenue:.2f}',
    }
    (GOLD / '_metadata' / 'reconciliation.json').write_text(json.dumps(reconciliation, indent=2), encoding='utf-8')

    total_units = sum(int(r['quantity']) for r in fact_sales)
    total_margin = sum(q(r['gross_margin']) for r in fact_sales)
    kpis = {
        'orders_recognized': recognized_orders,
        'revenue_recognized': float(recognized_revenue),
        'gross_margin': float(total_margin),
        'margin_pct_on_line_sales': float((total_margin / recognized_revenue * 100) if recognized_revenue else 0),
        'total_units_recognized_lines': total_units,
        'inventory_records': len(inv_rows),
        'critical_inventory_records': sum(r['stock_status'] == 'CRITICAL' for r in inv_rows),
    }
    (GOLD / '_metadata' / 'gold_kpis.json').write_text(json.dumps(kpis, indent=2), encoding='utf-8')
    print(json.dumps(kpis, indent=2))


if __name__ == '__main__':
    main()
