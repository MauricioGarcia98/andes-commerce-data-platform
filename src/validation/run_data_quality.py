from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SAMPLE = BASE / "data" / "sample"
OUT = BASE / "data" / "dq_results"

sys.path.append(str(BASE / "src"))
from validation.rules import (  # noqa: E402
    CheckResult,
    check_in_values,
    check_not_null,
    check_numeric_min,
    check_referential_integrity,
    check_unique,
    execute_check,
    read_csv,
)


def as_ids(rows, column):
    return {row[column] for row in rows if row.get(column)}


def run() -> list[CheckResult]:
    OUT.mkdir(parents=True, exist_ok=True)

    stores = read_csv(SAMPLE / "stores.csv")
    customers = read_csv(SAMPLE / "customers.csv")
    products = read_csv(SAMPLE / "products.csv")
    orders = read_csv(SAMPLE / "orders.csv")
    order_items = read_csv(SAMPLE / "order_items.csv")
    payments = read_csv(SAMPLE / "payments.csv")
    inventory = read_csv(SAMPLE / "inventory.csv")
    promotions = read_csv(SAMPLE / "promotions.csv")
    redemptions = read_csv(SAMPLE / "promotion_redemptions.csv")

    results: list[CheckResult] = []

    # Customers
    results += [
        execute_check("CUS-001", "customers", "customer_id NOT NULL", customers, check_not_null, "CRITICAL", column="customer_id"),
        execute_check("CUS-002", "customers", "customer_id UNIQUE", customers, check_unique, "CRITICAL", column="customer_id"),
        execute_check("CUS-003", "customers", "email NOT NULL", customers, check_not_null, "CRITICAL", column="email"),
    ]

    # Products
    results += [
        execute_check("PRD-001", "products", "product_id NOT NULL", products, check_not_null, "CRITICAL", column="product_id"),
        execute_check("PRD-002", "products", "product_id UNIQUE", products, check_unique, "CRITICAL", column="product_id"),
        execute_check("PRD-003", "products", "unit_cost >= 0", products, check_numeric_min, "CRITICAL", column="unit_cost", minimum=0),
        execute_check("PRD-004", "products", "list_price >= 0", products, check_numeric_min, "CRITICAL", column="list_price", minimum=0),
    ]

    # Orders
    results += [
        execute_check("ORD-001", "orders", "order_id UNIQUE", orders, check_unique, "CRITICAL", column="order_id"),
        execute_check("ORD-002", "orders", "customer_id references customers", orders, check_referential_integrity, "CRITICAL", fk_column="customer_id", ref_values=as_ids(customers, "customer_id")),
        execute_check("ORD-003", "orders", "status allowed", orders, check_in_values, "CRITICAL", column="status", allowed={"COMPLETED", "CANCELLED", "RETURNED", "PENDING"}),
        execute_check("ORD-004", "orders", "total_amount >= 0", orders, check_numeric_min, "CRITICAL", column="total_amount", minimum=0),
    ]

    # Order items
    results += [
        execute_check("ITM-001", "order_items", "order_item_id UNIQUE", order_items, check_unique, "CRITICAL", column="order_item_id"),
        execute_check("ITM-002", "order_items", "order_id references orders", order_items, check_referential_integrity, "CRITICAL", fk_column="order_id", ref_values=as_ids(orders, "order_id")),
        execute_check("ITM-003", "order_items", "product_id references products", order_items, check_referential_integrity, "CRITICAL", fk_column="product_id", ref_values=as_ids(products, "product_id")),
        execute_check("ITM-004", "order_items", "quantity > 0", order_items, check_numeric_min, "CRITICAL", column="quantity", minimum=1),
    ]

    # Payments
    results += [
        execute_check("PAY-001", "payments", "payment_id UNIQUE", payments, check_unique, "CRITICAL", column="payment_id"),
        execute_check("PAY-002", "payments", "order_id references orders", payments, check_referential_integrity, "CRITICAL", fk_column="order_id", ref_values=as_ids(orders, "order_id")),
        execute_check("PAY-003", "payments", "payment_status allowed", payments, check_in_values, "CRITICAL", column="payment_status", allowed={"APPROVED", "REJECTED", "REFUNDED"}),
        execute_check("PAY-004", "payments", "amount >= 0", payments, check_numeric_min, "CRITICAL", column="amount", minimum=0),
    ]

    # Inventory
    results += [
        execute_check("INV-001", "inventory", "product_id references products", inventory, check_referential_integrity, "CRITICAL", fk_column="product_id", ref_values=as_ids(products, "product_id")),
        execute_check("INV-002", "inventory", "store_id references stores", inventory, check_referential_integrity, "CRITICAL", fk_column="store_id", ref_values=as_ids(stores, "store_id")),
        execute_check("INV-003", "inventory", "on_hand_qty >= 0", inventory, check_numeric_min, "CRITICAL", column="on_hand_qty", minimum=0),
        execute_check("INV-004", "inventory", "reorder_point >= 0", inventory, check_numeric_min, "CRITICAL", column="reorder_point", minimum=0),
    ]

    # Promotions / redemptions
    results += [
        execute_check("PRO-001", "promotions", "promotion_id UNIQUE", promotions, check_unique, "CRITICAL", column="promotion_id"),
        execute_check("PRO-002", "promotions", "discount_pct >= 0", promotions, check_numeric_min, "CRITICAL", column="discount_pct", minimum=0),
        execute_check("RED-001", "promotion_redemptions", "order_id references orders", redemptions, check_referential_integrity, "CRITICAL", fk_column="order_id", ref_values=as_ids(orders, "order_id")),
        execute_check("RED-002", "promotion_redemptions", "promotion_id references promotions", redemptions, check_referential_integrity, "CRITICAL", fk_column="promotion_id", ref_values=as_ids(promotions, "promotion_id")),
    ]

    with (OUT / "dq_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CheckResult.__dataclass_fields__.keys())
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)

    total_checked = sum(r.records_checked for r in results)
    total_failed = sum(r.records_failed for r in results)
    score = 100.0 if total_checked == 0 else round((1 - total_failed / total_checked) * 100, 2)
    summary = {
        "checks": len(results),
        "checks_passed": sum(r.status == "PASS" for r in results),
        "checks_failed": sum(r.status == "FAIL" for r in results),
        "records_checked": total_checked,
        "records_failed": total_failed,
        "dq_score": score,
    }
    (OUT / "dq_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    for key, value in summary.items():
        print(f"{key}: {value}")
    return results


if __name__ == "__main__":
    run()
