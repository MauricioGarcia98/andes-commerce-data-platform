import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SILVER = BASE / 'data' / 'silver'


def rows(path):
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def test_silver_datasets_exist():
    expected = ['customers', 'products', 'stores', 'promotions', 'orders', 'order_items', 'payments', 'inventory', 'promotion_redemptions']
    for name in expected:
        assert (SILVER / f'{name}.csv').exists()


def test_order_items_have_derived_amounts():
    data = rows(SILVER / 'order_items.csv')
    assert data
    assert all('gross_amount' in r and 'net_amount' in r for r in data)


def test_silver_has_lineage():
    data = rows(SILVER / 'customers.csv')
    assert data
    assert all(r['source_run_id'] for r in data)
    assert all(r['record_hash'] for r in data)


def test_no_rejected_rows_in_clean_sample():
    assert not (BASE / 'data' / 'quarantine' / 'customers.csv').exists()
