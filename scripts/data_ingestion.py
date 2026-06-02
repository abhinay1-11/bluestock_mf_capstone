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

def explore_fund_master(df):
    print("\n" + "="*50)
    print("FUND MASTER EXPLORATION")
    print("="*50)

    print("\nUnique Fund Houses:")
    print(df["fund_house"].unique())

    print("\nUnique Categories:")
    print(df["category"].unique())

    print("\nUnique Sub Categories:")
    print(df["sub_category"].unique())

    print("\nUnique Risk Grades:")
    print(df["risk_category"].unique())

    print(f"\nTotal Schemes : {len(df)}")
    print(f"Unique AMFI Codes : {df['amfi_code'].nunique()}")

explore_fund_master(datasets["01_fund_master.csv"])

def validate_amfi_codes(fund_master, nav_history):
    print("\n" + "="*50)
    print("AMFI CODE VALIDATION")
    print("="*50)

    fm_codes  = set(fund_master["amfi_code"].dropna().astype(int))
    nav_codes = set(nav_history["amfi_code"].dropna().astype(int))

    missing = fm_codes - nav_codes
    coverage = (len(fm_codes - missing) / len(fm_codes)) * 100

    print(f"\nFund Master codes : {len(fm_codes)}")
    print(f"NAV History codes : {len(nav_codes)}")
    print(f"Missing in NAV    : {len(missing)}")
    print(f"Coverage          : {coverage:.1f}%")

    if missing:
        print(f"Missing codes: {missing}")
    else:
        print("All fund_master codes exist in nav_history!")

validate_amfi_codes(datasets["01_fund_master.csv"], datasets["02_nav_history.csv"])