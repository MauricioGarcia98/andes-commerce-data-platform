from pathlib import Path
import csv, sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng
from common.io_utils import write_csv

BASE = Path(__file__).resolve().parents[1]
OUT = BASE/"data"/"sample"/"promotion_redemptions.csv"

def generate(n=1200, seed=42):
    rng = get_rng(seed)
    orders = list(csv.DictReader((BASE/"data"/"sample"/"orders.csv").open(encoding="utf-8")))
    promotions = list(csv.DictReader((BASE/"data"/"sample"/"promotions.csv").open(encoding="utf-8")))
    rows = []
    for i in range(1, n+1):
        order = rng.choice(orders)
        promo = rng.choice(promotions)
        rows.append({
            "redemption_id": f"RED-{i:07d}",
            "order_id": order["order_id"],
            "promotion_id": promo["promotion_id"],
            "discount_amount": round(rng.uniform(2, 75), 2),
        })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
