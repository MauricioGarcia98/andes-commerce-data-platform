from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
scripts = [
    "generate_stores.py",
    "generate_customers.py",
    "generate_products.py",
    "generate_promotions.py",
    "generate_orders.py",
    "generate_order_items.py",
    "reconcile_order_totals.py",
    "generate_payments.py",
    "generate_inventory.py",
    "generate_promotion_redemptions.py",
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run([sys.executable, str(BASE/script)], check=True)

print("All generators completed.")
