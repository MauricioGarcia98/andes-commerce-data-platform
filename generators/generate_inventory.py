from pathlib import Path
import csv, sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng
from common.io_utils import write_csv

BASE = Path(__file__).resolve().parents[1]
OUT = BASE/"data"/"sample"/"inventory.csv"

def generate(seed=42):
    rng = get_rng(seed)
    products = list(csv.DictReader((BASE/"data"/"sample"/"products.csv").open(encoding="utf-8")))
    stores = list(csv.DictReader((BASE/"data"/"sample"/"stores.csv").open(encoding="utf-8")))
    rows = []
    for p in products:
        for s in stores:
            on_hand = rng.randint(0, 250)
            reorder_point = rng.randint(5, 50)
            rows.append({
                "product_id": p["product_id"],
                "store_id": s["store_id"],
                "snapshot_date": "2026-08-31",
                "on_hand_qty": on_hand,
                "reorder_point": reorder_point,
                "stock_status": "CRITICAL" if on_hand <= reorder_point else ("LOW" if on_hand <= reorder_point * 2 else "HEALTHY"),
            })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
