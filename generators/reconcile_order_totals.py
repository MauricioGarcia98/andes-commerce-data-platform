from pathlib import Path
import csv
from collections import defaultdict

BASE = Path(__file__).resolve().parents[1]
ORDERS = BASE / "data" / "sample" / "orders.csv"
ITEMS = BASE / "data" / "sample" / "order_items.csv"


def reconcile():
    totals = defaultdict(float)

    with ITEMS.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            totals[row["order_id"]] += (
                float(row["quantity"]) * float(row["unit_price"])
                - float(row["discount_amount"])
            )

    with ORDERS.open(encoding="utf-8", newline="") as f:
        orders = list(csv.DictReader(f))

    if not orders:
        raise ValueError("orders.csv está vacío.")

    missing = [row["order_id"] for row in orders if row["order_id"] not in totals]
    if missing:
        raise ValueError(
            f"Hay {len(missing)} orders sin order_items. Ejemplos: {missing[:5]}"
        )

    for row in orders:
        row["total_amount"] = f'{totals[row["order_id"]]:.2f}'

    with ORDERS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)

    print(f"Reconciled {len(orders)} orders from {sum(1 for _ in totals)} order groups.")


if __name__ == "__main__":
    reconcile()
