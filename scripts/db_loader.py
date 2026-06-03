import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR      = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR       = BASE_DIR / "data" / "raw"
DB_PATH       = BASE_DIR / "data" / "db" / "bluestock_mf.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

def load_data():
    print("\n" + "="*50)
    print("Loading data into SQLite database")
    print("="*50)

    # Load dim_fund
    df_fund = pd.read_csv(RAW_DIR / "01_fund_master.csv")
    df_fund.to_sql("dim_fund", engine, if_exists="replace", index=False)
    print(f"dim_fund loaded: {len(df_fund)} rows")

    # Load fact_nav
    df_nav = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv")
    df_nav.to_sql("fact_nav", engine, if_exists="replace", index=False)
    print(f"fact_nav loaded: {len(df_nav)} rows")

    # Load fact_transactions
    df_txn = pd.read_csv(PROCESSED_DIR / "clean_investor_transactions.csv")
    df_txn.to_sql("fact_transactions", engine, if_exists="replace", index=False)
    print(f"fact_transactions loaded: {len(df_txn)} rows")

    # Load fact_performance
    df_perf = pd.read_csv(PROCESSED_DIR / "clean_scheme_performance.csv")
    df_perf.to_sql("fact_performance", engine, if_exists="replace", index=False)
    print(f"fact_performance loaded: {len(df_perf)} rows")

    # Load fact_aum
    df_aum = pd.read_csv(RAW_DIR / "03_aum_by_fund_house.csv")
    df_aum.to_sql("fact_aum", engine, if_exists="replace", index=False)
    print(f"fact_aum loaded: {len(df_aum)} rows")

    print("\nAll tables loaded successfully!")

if __name__ == "__main__":
    load_data()