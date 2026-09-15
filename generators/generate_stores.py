from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng
from common.io_utils import write_csv

OUT = Path(__file__).resolve().parents[1] / "data" / "sample" / "stores.csv"

def generate(n=12, seed=42):
    rng = get_rng(seed)
    cities = [
        ("Buenos Aires", "AMBA"),
        ("Córdoba", "Centro"),
        ("Rosario", "Litoral"),
        ("Mendoza", "Cuyo"),
        ("La Plata", "AMBA"),
        ("Mar del Plata", "Buenos Aires"),
    ]
    rows = []
    for i in range(1, n + 1):
        city, region = rng.choice(cities)
        rows.append({
            "store_id": f"STORE-{i:04d}",
            "store_name": f"Andes Store {i:02d}",
            "city": city,
            "region": region,
            "channel": "STORE",
            "active_flag": True,
        })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
