from pathlib import Path
from datetime import date
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng, random_date
from common.io_utils import write_csv

OUT = Path(__file__).resolve().parents[1] / "data" / "sample" / "customers.csv"

def generate(n=1000, seed=42):
    rng = get_rng(seed)
    first_names = ["Lucia", "Mateo", "Sofia", "Juan", "Camila", "Nicolas", "Valentina", "Martin", "Agustin", "Paula"]
    last_names = ["Gomez", "Fernandez", "Rodriguez", "Lopez", "Martinez", "Diaz", "Sanchez", "Romero", "Torres", "Acosta"]
    cities = ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata"]
    segments = ["STANDARD", "PREMIUM", "BUSINESS"]
    rows = []
    for i in range(1, n + 1):
        fn, ln = rng.choice(first_names), rng.choice(last_names)
        rows.append({
            "customer_id": f"CUST-{i:06d}",
            "first_name": fn,
            "last_name": ln,
            "email": f"{fn.lower()}.{ln.lower()}.{i}@example.com",
            "signup_date": random_date(rng, date(2023,1,1), date(2026,8,31)).isoformat(),
            "customer_segment": rng.choices(segments, weights=[70,25,5], k=1)[0],
            "city": rng.choice(cities),
        })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
