from pathlib import Path
from datetime import date
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng, random_date
from common.io_utils import write_csv

OUT = Path(__file__).resolve().parents[1] / "data" / "sample" / "promotions.csv"

def generate(n=30, seed=42):
    rng = get_rng(seed)
    names = ["WELCOME", "HOTSALE", "SEASONAL", "LOYALTY", "FLASH"]
    rows = []
    for i in range(1, n+1):
        start = random_date(rng, date(2025,1,1), date(2026,7,1))
        end = min(start.replace(year=start.year + 1), date(2026,8,31))
        rows.append({
            "promotion_id": f"PROMO-{i:04d}",
            "promotion_name": f"{rng.choice(names)}-{i:02d}",
            "discount_pct": rng.choice([5, 10, 15, 20, 25]),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "active_flag": end >= date(2026,1,1),
        })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
