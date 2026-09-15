from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BRONZE = BASE / 'data' / 'bronze'
SILVER = BASE / 'data' / 'silver'
QUARANTINE = BASE / 'data' / 'quarantine'
METADATA = SILVER / '_metadata'

PRIMARY_KEYS = {
    'customers': ['customer_id'],
    'products': ['product_id'],
    'stores': ['store_id'],
    'promotions': ['promotion_id'],
    'orders': ['order_id'],
    'order_items': ['order_item_id'],
    'payments': ['payment_id'],
    'inventory': ['product_id', 'store_id', 'snapshot_date'],
    'promotion_redemptions': ['redemption_id'],
}

DATE_COLUMNS = {
    'customers': ['signup_date'],
    'promotions': ['start_date', 'end_date'],
    'orders': ['order_date'],
    'inventory': ['snapshot_date'],
}

DECIMAL_COLUMNS = {
    'products': ['unit_cost', 'list_price'],
    'orders': ['total_amount'],
    'order_items': ['unit_price', 'discount_amount'],
    'payments': ['amount'],
    'promotion_redemptions': ['discount_amount'],
}

INTEGER_COLUMNS = {
    'order_items': ['quantity'],
    'inventory': ['on_hand_qty', 'reorder_point'],
}

UPPER_COLUMNS = {
    'customers': ['customer_segment'],
    'stores': ['region', 'channel'],
    'orders': ['channel', 'status'],
    'payments': ['payment_method', 'payment_status'],
    'inventory': ['stock_status'],
}

ALLOWED = {
    ('customers', 'customer_segment'): {'STANDARD', 'PREMIUM', 'BUSINESS'},
    ('stores', 'channel'): {'STORE', 'ECOMMERCE'},
    ('orders', 'channel'): {'STORE', 'ECOMMERCE'},
    ('orders', 'status'): {'COMPLETED', 'CANCELLED', 'RETURNED', 'PENDING'},
    ('payments', 'payment_method'): {'CARD', 'CASH', 'TRANSFER', 'WALLET'},
    ('payments', 'payment_status'): {'APPROVED', 'REJECTED', 'REFUNDED'},
}


def latest_bronze_run() -> Path:
    runs = [p for p in BRONZE.iterdir() if p.is_dir() and p.name != '_metadata']
    if not runs:
        raise FileNotFoundError('No Bronze run found. Run ingestion first.')
    return sorted(runs)[-1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def normalize(value: str | None) -> str:
    return '' if value is None else value.strip()


def to_decimal(value: str) -> str:
    d = Decimal(value)
    return f'{d:.2f}'


def to_int(value: str) -> str:
    return str(int(value))


def row_hash(row: dict[str, object]) -> str:
    payload = '|'.join(f'{k}={row.get(k, "")}' for k in sorted(row))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def transform_dataset(name: str, rows: list[dict[str, str]], source_run_id: str):
    accepted: list[dict[str, object]] = []
    rejected: list[dict[str, object]] = []
    seen_keys: set[tuple[str, ...]] = set()

    for row_number, raw in enumerate(rows, start=2):
        row = {k: normalize(v) for k, v in raw.items()}
        issues: list[str] = []

        for col in UPPER_COLUMNS.get(name, []):
            if row.get(col):
                row[col] = row[col].upper()

        for col in DATE_COLUMNS.get(name, []):
            if row.get(col):
                try:
                    datetime.strptime(row[col], '%Y-%m-%d')
                except ValueError:
                    issues.append(f'invalid_date:{col}')

        for col in DECIMAL_COLUMNS.get(name, []):
            if row.get(col):
                try:
                    row[col] = to_decimal(row[col])
                except (InvalidOperation, ValueError):
                    issues.append(f'invalid_decimal:{col}')

        for col in INTEGER_COLUMNS.get(name, []):
            if row.get(col):
                try:
                    row[col] = to_int(row[col])
                except ValueError:
                    issues.append(f'invalid_integer:{col}')

        for (dataset, col), allowed in ALLOWED.items():
            if dataset == name and row.get(col) not in allowed:
                issues.append(f'invalid_domain:{col}')

        key = tuple(row.get(col, '') for col in PRIMARY_KEYS[name])
        if any(v == '' for v in key):
            issues.append('missing_primary_key')
        elif key in seen_keys:
            issues.append('duplicate_primary_key')
        else:
            seen_keys.add(key)

        if name == 'products':
            try:
                if Decimal(row['list_price']) < Decimal(row['unit_cost']):
                    issues.append('list_price_below_unit_cost')
            except (KeyError, InvalidOperation):
                pass

        if name == 'order_items':
            try:
                qty = int(row['quantity'])
                unit = Decimal(row['unit_price'])
                disc = Decimal(row['discount_amount'])
                if qty <= 0:
                    issues.append('quantity_not_positive')
                if disc < 0:
                    issues.append('discount_negative')
                row['gross_amount'] = f'{qty * unit:.2f}'
                row['net_amount'] = f'{qty * unit - disc:.2f}'
            except (KeyError, InvalidOperation, ValueError):
                issues.append('order_item_calculation_error')

        row['source_run_id'] = source_run_id
        row['source_row_number'] = row_number
        row['silver_processed_at_utc'] = datetime.now(timezone.utc).isoformat()
        row['record_hash'] = row_hash(row)

        if issues:
            row['dq_status'] = 'REJECTED'
            row['dq_reasons'] = ';'.join(sorted(set(issues)))
            rejected.append(row)
        else:
            row['dq_status'] = 'ACCEPTED'
            row['dq_reasons'] = ''
            accepted.append(row)

    return accepted, rejected


def main() -> None:
    source_dir = latest_bronze_run()
    source_run_id = source_dir.name
    SILVER.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)

    summary = []

    for source_file in sorted(source_dir.glob('*.csv')):
        name = source_file.stem
        rows = read_csv(source_file)
        accepted, rejected = transform_dataset(name, rows, source_run_id)

        if accepted:
            fields = list(accepted[0].keys())
        elif rejected:
            fields = list(rejected[0].keys())
        else:
            fields = []

        write_csv(SILVER / f'{name}.csv', accepted, fields)
        if rejected:
            write_csv(QUARANTINE / f'{name}.csv', rejected, fields)

        summary.append({
            'source_run_id': source_run_id,
            'dataset': name,
            'bronze_records': len(rows),
            'silver_records': len(accepted),
            'quarantined_records': len(rejected),
            'silver_acceptance_rate': round(len(accepted) / len(rows) * 100, 2) if rows else 100.0,
            'processed_at_utc': datetime.now(timezone.utc).isoformat(),
        })

    write_csv(METADATA / 'silver_run_summary.csv', summary, list(summary[0].keys()) if summary else [])
    totals = {
        'source_run_id': source_run_id,
        'datasets': len(summary),
        'bronze_records': sum(x['bronze_records'] for x in summary),
        'silver_records': sum(x['silver_records'] for x in summary),
        'quarantined_records': sum(x['quarantined_records'] for x in summary),
    }
    (METADATA / 'silver_run_summary.json').write_text(json.dumps(totals, indent=2), encoding='utf-8')
    print(json.dumps(totals, indent=2))


if __name__ == '__main__':
    main()
