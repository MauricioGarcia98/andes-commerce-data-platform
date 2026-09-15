from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SOURCE = BASE / "data" / "sample"
BRONZE = BASE / "data" / "bronze"
METADATA = BRONZE / "_metadata"


def ingest() -> None:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = BRONZE / run_id
    target.mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)

    rows = []
    for source_file in sorted(SOURCE.glob("*.csv")):
        destination = target / source_file.name
        shutil.copy2(source_file, destination)
        rows.append({
            "run_id": run_id,
            "source_file": source_file.name,
            "source_path": str(source_file.relative_to(BASE)),
            "target_path": str(destination.relative_to(BASE)),
            "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": "SUCCESS",
        })

    metadata_file = METADATA / "ingestion_log.csv"
    with metadata_file.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        if metadata_file.stat().st_size == 0:
            writer.writeheader()
        writer.writerows(rows)

    print(f"Bronze ingestion completed: {run_id}")
    print(f"Files ingested: {len(rows)}")
    print(f"Target: {target}")


if __name__ == "__main__":
    ingest()
