from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from validation.rules import check_not_null, check_unique, check_numeric_min


def test_not_null_detects_missing_value():
    rows = [{"id":"1"}, {"id":""}]
    failed, _ = check_not_null(rows, "x", "id")
    assert failed == 1


def test_unique_detects_duplicate():
    rows = [{"id":"1"}, {"id":"1"}, {"id":"2"}]
    failed, _ = check_unique(rows, "x", "id")
    assert failed == 1


def test_numeric_min_detects_negative():
    rows = [{"amount":"10"}, {"amount":"-2"}]
    failed, _ = check_numeric_min(rows, "x", "amount", minimum=0)
    assert failed == 1
