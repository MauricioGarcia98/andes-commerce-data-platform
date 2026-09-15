from pathlib import Path
import csv, sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng
from common.io_utils import write_csv

BASE = Path(__file__).resolve().parents[1]
OUT = BASE/"data"/"sample"/"payments.csv"

def generate(seed=42):
    rng = get_rng(seed)
    orders = list(csv.DictReader((BASE/"data"/"sample"/"orders.csv").open(encoding="utf-8")))
    methods = ["CARD", "CASH", "TRANSFER", "WALLET"]
    statuses = ["APPROVED", "REJECTED", "REFUNDED"]
    rows = []
    for i, order in enumerate(orders, 1):
        order_status = order["status"]
        pay_status = "APPROVED" if order_status == "COMPLETED" else rng.choices(statuses, weights=[50,20,30], k=1)[0]
        rows.append({
            "payment_id": f"PAY-{i:08d}",
            "order_id": order["order_id"],
            "payment_method": rng.choice(methods),
            "payment_status": pay_status,
            "amount": float(order["total_amount"]) if pay_status == "APPROVED" else 0.0,
        })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
