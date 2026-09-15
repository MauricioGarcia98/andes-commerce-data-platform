from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.random_utils import get_rng
from common.io_utils import write_csv

OUT = Path(__file__).resolve().parents[1] / "data" / "sample" / "products.csv"

def generate(n=300, seed=42):
    rng = get_rng(seed)
    catalog = {
        "Electronics": ["Headphones", "Keyboard", "Mouse", "Monitor", "Webcam"],
        "Home": ["Lamp", "Chair", "Desk", "Pan", "Vacuum"],
        "Sports": ["Ball", "Shoes", "Jersey", "Mat", "Bottle"],
        "Beauty": ["Shampoo", "Cream", "Perfume", "Soap", "Serum"],
        "Grocery": ["Coffee", "Tea", "Cereal", "Pasta", "Oil"],
    }
    rows = []
    categories = list(catalog)
    for i in range(1, n + 1):
        cat = rng.choice(categories)
        name = rng.choice(catalog[cat])
        unit_cost = round(rng.uniform(2, 150), 2)
        list_price = round(unit_cost * rng.uniform(1.20, 2.20), 2)
        rows.append({
            "product_id": f"PROD-{i:06d}",
            "sku": f"SKU-{i:06d}",
            "product_name": f"{name} {i:03d}",
            "category": cat,
            "unit_cost": unit_cost,
            "list_price": list_price,
            "active_flag": rng.random() < 0.96,
        })
    write_csv(OUT, rows, rows[0].keys())

if __name__ == "__main__":
    generate()
