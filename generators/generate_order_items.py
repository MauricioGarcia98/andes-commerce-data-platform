from pathlib import Path
import csv, sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng
from common.io_utils import write_csv

BASE = Path(__file__).resolve().parents[1]
OUT = BASE/"data"/"sample"/"order_items.csv"

def generate(n_per_order=2, seed=42):
    rng = get_rng(seed)
    orders = list(csv.DictReader((BASE/"data"/"sample"/"orders.csv").open(encoding="utf-8")))
    products = list(csv.DictReader((BASE/"data"/"sample"/"products.csv").open(encoding="utf-8")))
    rows = []
    idx = 1
    for order in orders:
        count = rng.randint(1, n_per_order + 2)
        for _ in range(count):
            p = rng.choice(products)
            rows.append({
                "order_item_id": f"ITEM-{idx:09d}",
                "order_id": order["order_id"],
                "product_id": p["product_id"],
                "quantity": rng.randint(1, 5),
                "unit_price": float(p["list_price"]),
                "discount_amount": round(rng.uniform(0, float(p["list_price"]) * 0.20), 2),
            })
            idx += 1
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
