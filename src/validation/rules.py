from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    dataset: str
    rule: str
    severity: str
    records_checked: int
    records_failed: int
    status: str
    message: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def check_not_null(rows, dataset, column, severity="CRITICAL"):
    failed = sum(1 for row in rows if str(row.get(column, "")).strip() == "")
    return failed, f"{column} must not be null or empty"


def check_unique(rows, dataset, column, severity="CRITICAL"):
    seen = set()
    duplicates = 0
    for row in rows:
        value = row.get(column, "")
        if value in seen:
            duplicates += 1
        else:
            seen.add(value)
    return duplicates, f"{column} must be unique"


def check_numeric_min(rows, dataset, column, minimum=0, severity="CRITICAL"):
    failed = 0
    for row in rows:
        try:
            value = Decimal(row.get(column, ""))
            if value < Decimal(str(minimum)):
                failed += 1
        except (InvalidOperation, ValueError):
            failed += 1
    return failed, f"{column} must be numeric and >= {minimum}"


def check_in_values(rows, dataset, column, allowed, severity="CRITICAL"):
    allowed = set(allowed)
    failed = sum(1 for row in rows if row.get(column) not in allowed)
    return failed, f"{column} must be one of: {', '.join(sorted(allowed))}"


def check_referential_integrity(rows, dataset, fk_column, ref_values, severity="CRITICAL"):
    failed = sum(1 for row in rows if row.get(fk_column, "") and row.get(fk_column) not in ref_values)
    return failed, f"{fk_column} must exist in referenced dataset"


def execute_check(check_id, dataset, rule, rows, fn, severity, **kwargs):
    failed, message = fn(rows, dataset, **kwargs)
    status = "PASS" if failed == 0 else "FAIL"
    return CheckResult(
        check_id=check_id,
        dataset=dataset,
        rule=rule,
        severity=severity,
        records_checked=len(rows),
        records_failed=failed,
        status=status,
        message=message,
    )
