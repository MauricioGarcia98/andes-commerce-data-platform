from pathlib import Path

def test_generators_are_independent():
    path = Path(__file__).resolve().parents[1] / "generators"
    expected = [
        "generate_customers.py",
        "generate_products.py",
        "generate_stores.py",
        "generate_orders.py",
        "generate_order_items.py",
        "generate_payments.py",
        "generate_inventory.py",
    ]
    for name in expected:
        assert (path / name).exists(), f"Missing generator: {name}"
