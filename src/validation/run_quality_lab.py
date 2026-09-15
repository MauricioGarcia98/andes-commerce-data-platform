from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SAMPLE = BASE / "data" / "sample"
OUT = BASE / "data" / "quality_lab"


def load(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    orders = load(SAMPLE / "orders.csv")
    fields = list(orders[0].keys())
    broken = [dict(r) for r in orders[:20]]

    # Incident 1: duplicate natural/business key.
    broken.append(dict(broken[0]))

    # Incident 2: invalid foreign key.
    broken[1]["customer_id"] = "CUST-NOT-EXIST"

    # Incident 3: negative amount.
    broken[2]["total_amount"] = "-50.00"

    # Incident 4: unsupported status.
    broken[3]["status"] = "UNKNOWN_STATUS"

    write(OUT / "orders_with_incidents.csv", broken, fields)

    incident_catalog = [
        {"incident_id":"INC-DQ-001","type":"DUPLICATE","column":"order_id","expected_behavior":"Reject duplicate key and preserve evidence."},
        {"incident_id":"INC-DQ-002","type":"REFERENTIAL_INTEGRITY","column":"customer_id","expected_behavior":"Fail the relationship check and quarantine the record."},
        {"incident_id":"INC-DQ-003","type":"DOMAIN_RULE","column":"total_amount","expected_behavior":"Reject negative monetary value."},
        {"incident_id":"INC-DQ-004","type":"INVALID_ENUM","column":"status","expected_behavior":"Reject unsupported status value."},
    ]
    write(OUT / "incident_catalog.csv", incident_catalog, list(incident_catalog[0].keys()))

    (OUT / "README.md").write_text(
        "# Quality Lab\n\nEste dataset es deliberadamente defectuoso. No pertenece al flujo productivo.\n\nSirve para practicar troubleshooting e entrevistas. Los incidentes representan: duplicados, foreign keys inválidas, valores monetarios negativos y dominios no permitidos.\n",
        encoding="utf-8",
    )
    print("Quality lab created")


if __name__ == "__main__":
    build()
