from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture(scope="session", autouse=True)
def build_local_pipeline():
    """Build reproducible local artifacts from sample sources for integration tests."""
    commands = [
        [sys.executable, "generators/run_all_generators.py"],
        [sys.executable, "src/ingestion/bronze_ingestion.py"],
        [sys.executable, "src/validation/run_data_quality.py"],
        [sys.executable, "src/transformation/silver_transform.py"],
        [sys.executable, "src/transformation/build_gold.py"],
    ]
    for command in commands:
        subprocess.run(command, cwd=ROOT, check=True)
    yield
