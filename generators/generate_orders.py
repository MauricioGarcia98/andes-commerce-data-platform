from pathlib import Path
from datetime import date
import csv
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng, random_date
from common.io_utils import write_csv

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "data" / "sample" / "orders.csv"

def generate(n=5000, seed=42):
    rng = get_rng(seed)
    customers = list(csv.DictReader((BASE/"data"/"sample"/"customers.csv").open(encoding="utf-8")))
    stores = list(csv.DictReader((BASE/"data"/"sample"/"stores.csv").open(encoding="utf-8")))
    rows = []
    statuses = ["COMPLETED", "CANCELLED", "RETURNED", "PENDING"]
    channels = ["STORE", "ECOMMERCE"]
    for i in range(1, n+1):
        channel = rng.choices(channels, weights=[65,35], k=1)[0]
        rows.append({
            "order_id": f"ORD-{i:08d}",
            "customer_id": rng.choice(customers)["customer_id"],
            "store_id": rng.choice(stores)["store_id"] if channel == "STORE" else "",
            "order_date": random_date(rng, date(2025,1,1), date(2026,8,31)).isoformat(),
            "channel": channel,
            "status": rng.choices(statuses, weights=[88,4,6,2], k=1)[0],
            "total_amount": round(rng.uniform(15, 900), 2),
        })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
