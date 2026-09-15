from pathlib import Path
import csv, json

BASE = Path(__file__).resolve().parents[1]
GOLD = BASE / "data" / "gold"


def read_csv(name):
    with (GOLD / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_gold_files_exist():
    expected = [
        "dim_customer.csv", "dim_product.csv", "dim_store.csv", "dim_promotion.csv", "dim_date.csv",
        "fact_sales_line.csv", "fact_order.csv", "fact_inventory_snapshot.csv",
        "mart_sales_by_category.csv", "mart_sales_by_channel.csv", "mart_store_performance.csv",
        "mart_inventory_risk.csv", "mart_customer_value.csv",
    ]
    for name in expected:
        assert (GOLD / name).exists()


def test_gold_reconciliation():
    recon = json.loads((GOLD / "_metadata" / "reconciliation.json").read_text(encoding="utf-8"))
    assert recon["completed_approved_orders_source"] == recon["orders_with_recognized_revenue_gold"]
    assert float(recon["recognized_revenue"]) > 0


def test_sales_line_has_unique_order_items():
    rows = read_csv("fact_sales_line.csv")
    ids = [r["order_item_id"] for r in rows]
    assert len(ids) == len(set(ids))


def test_inventory_risk_categories():
    rows = read_csv("mart_inventory_risk.csv")
    allowed = {"CRITICAL", "LOW", "HEALTHY"}
    assert rows
    assert set(r["stock_status"] for r in rows).issubset(allowed)
