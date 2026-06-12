"""
run_pipeline.py
Bluestock MF Capstone — Master Pipeline Script
Runs the complete ETL pipeline in sequence:
1. Data ingestion (load + profile all 10 CSVs)
2. Live NAV fetch from mfapi.in
3. Data cleaning (nav, transactions, performance)
4. Load all data into SQLite database
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS  = BASE_DIR / "scripts"


def run_script(script_name: str) -> bool:
    """Run a Python script and return True if successful."""
    path = SCRIPTS / script_name
    print(f"\n{'='*60}")
    print(f"  Running: {script_name}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=False
    )

    if result.returncode == 0:
        print(f"  ✅ {script_name} completed successfully")
        return True
    else:
        print(f"  ❌ {script_name} failed with error code {result.returncode}")
        return False


def main():
    print("\n" + "="*60)
    print("  Bluestock MF Capstone — Full Pipeline")
    print("="*60)

    steps = [
        "data_ingestion.py",
        "live_nav_fetch.py",
        "data_cleaning.py",
        "db_loader.py",
    ]

    results = []
    for step in steps:
        success = run_script(step)
        results.append((step, success))

    # Summary
    print("\n" + "="*60)
    print("  Pipeline Summary")
    print("="*60)
    for step, success in results:
        status = "✅ Success" if success else "❌ Failed"
        print(f"  {step:<30} {status}")

    all_passed = all(r[1] for r in results)
    if all_passed:
        print("\n  🎉 Full pipeline completed successfully!")
    else:
        print("\n  ⚠️  Some steps failed. Check output above.")


if __name__ == "__main__":
    main()