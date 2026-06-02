import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR  = BASE_DIR / "data" / "raw"

CSV_FILES = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

def load_and_profile(filename):
    path = RAW_DIR / filename
    print("\n" + "="*50)
    print(f"File: {filename}")
    print("="*50)

    df = pd.read_csv(path)

    print(f"Shape   : {df.shape}")
    print(f"\ndtypes:\n{df.dtypes}")
    print(f"\nhead():\n{df.head()}")

    return df

datasets = {}

for filename in CSV_FILES:
    df = load_and_profile(filename)
    datasets[filename] = df

print("\n" + "="*50)
print(f"Successfully loaded {len(datasets)} datasets")
print("="*50)