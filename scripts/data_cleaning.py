import pandas as pd
import numpy  as np
from pathlib import Path

BASE_DIR      = Path(__file__).resolve().parent.parent
RAW_DIR       = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def clean_nav_history():
    print("\n" + "="*50)
    print("Cleaning nav_history.csv")
    print("="*50)

    df = pd.read_csv(RAW_DIR / "02_nav_history.csv")
    print(f"Original shape: {df.shape}")

    # Parse dates
    df["date"] = pd.to_datetime(df["date"])

    # Sort by amfi_code and date
    df = df.sort_values(["amfi_code", "date"])

    # Remove duplicates
    df = df.drop_duplicates(subset=["amfi_code", "date"])

    # Forward fill missing NAV for weekends/holidays
    all_dates = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    funds = df["amfi_code"].unique()
    idx = pd.MultiIndex.from_product([funds, all_dates], names=["amfi_code", "date"])
    df = df.set_index(["amfi_code", "date"]).reindex(idx).groupby(level="amfi_code").ffill()
    df = df.reset_index()
    
    # Validate NAV > 0
    invalid = df[df["nav"] <= 0]
    print(f"Invalid NAV rows (<=0): {len(invalid)}")
    df = df[df["nav"] > 0]

    print(f"Cleaned shape: {df.shape}")
    df.to_csv(PROCESSED_DIR / "clean_nav_history.csv", index=False)
    print("Saved → clean_nav_history.csv")

    return df

def clean_investor_transactions():
    print("\n" + "="*50)
    print("Cleaning investor_transactions.csv")
    print("="*50)

    df = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
    print(f"Original shape: {df.shape}")

    # Fix date format
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # Standardise transaction_type values
    valid_types = ["SIP", "Lumpsum", "Redemption"]
    invalid_types = df[~df["transaction_type"].isin(valid_types)]
    print(f"Invalid transaction types: {len(invalid_types)}")
    df = df[df["transaction_type"].isin(valid_types)]

    # Validate amount > 0
    invalid_amount = df[df["amount_inr"] <= 0]
    print(f"Invalid amounts (<=0): {len(invalid_amount)}")
    df = df[df["amount_inr"] > 0]

    # Check KYC status values
    valid_kyc = ["Verified", "Pending"]
    invalid_kyc = df[~df["kyc_status"].isin(valid_kyc)]
    print(f"Invalid KYC status rows: {len(invalid_kyc)}")
    df = df[df["kyc_status"].isin(valid_kyc)]

    # Remove duplicates
    df = df.drop_duplicates()

    print(f"Cleaned shape: {df.shape}")
    df.to_csv(PROCESSED_DIR / "clean_investor_transactions.csv", index=False)
    print("Saved → clean_investor_transactions.csv")

    return df
def clean_scheme_performance():
    print("\n" + "="*50)
    print("Cleaning scheme_performance.csv")
    print("="*50)

    df = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")
    print(f"Original shape: {df.shape}")

    # Validate return columns are numeric
    return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        nulls = df[col].isnull().sum()
        if nulls:
            print(f"Non-numeric values in {col}: {nulls}")

    # Flag negative Sharpe ratios
    negative_sharpe = df[df["sharpe_ratio"] < 0]
    print(f"Funds with negative Sharpe ratio: {len(negative_sharpe)}")
    if len(negative_sharpe) > 0:
        print(negative_sharpe[["scheme_name", "sharpe_ratio"]])

    # Check expense ratio range (0.1% - 2.5%)
    out_of_range = df[
        (df["expense_ratio_pct"] < 0.1) |
        (df["expense_ratio_pct"] > 2.5)
    ]
    print(f"Expense ratio out of range (0.1-2.5%): {len(out_of_range)}")
    if len(out_of_range) > 0:
        print(out_of_range[["scheme_name", "expense_ratio_pct"]])

    # Remove duplicates
    df = df.drop_duplicates()

    print(f"Cleaned shape: {df.shape}")
    df.to_csv(PROCESSED_DIR / "clean_scheme_performance.csv", index=False)
    print("Saved → clean_scheme_performance.csv")

    return df

def main():
    print("\n" + "="*50)
    print("Bluestock MF Capstone — Data Cleaning (Day 2)")
    print("="*50)

    nav        = clean_nav_history()
    txn        = clean_investor_transactions()
    perf       = clean_scheme_performance()

    print("\n" + "="*50)
    print("All cleaning complete!")
    print(f"nav_history        : {nav.shape}")
    print(f"investor_txn       : {txn.shape}")
    print(f"scheme_performance : {perf.shape}")
    print("="*50)

if __name__ == "__main__":
    main()