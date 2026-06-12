"""
recommender.py
Bluestock MF Capstone — Day 6
Simple fund recommender based on investor risk appetite.
Input : risk appetite (Low / Moderate / High / Very High)
Output: Top 3 funds by Sharpe ratio within matching risk_grade
"""

import pandas as pd
from pathlib import Path

BASE_DIR      = Path(__file__).resolve().parent.parent
RAW_DIR       = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def recommend_funds(risk_appetite: str) -> pd.DataFrame:
    """Return top 3 funds matching the given risk appetite."""

    # Load data
    fund   = pd.read_csv(RAW_DIR / "01_fund_master.csv")
    sharpe = pd.read_csv(PROCESSED_DIR / "sharpe_values.csv")

    # Merge
    df = sharpe.merge(
        fund[["amfi_code", "risk_category", "expense_ratio_pct", "fund_house"]],
        on="amfi_code"
    )

    # Normalize input
    risk_map = {
        "low"       : "Low",
        "moderate"  : "Moderate",
        "high"      : "High",
        "very high" : "Very High"
    }
    risk = risk_map.get(risk_appetite.lower().strip())

    if not risk:
        print(f"Invalid risk appetite. Choose: Low / Moderate / High / Very High")
        return pd.DataFrame()

    # Filter and rank
    filtered = df[df["risk_category"] == risk].sort_values(
        "sharpe_ratio", ascending=False
    ).head(3)

    if filtered.empty:
        print(f"No funds found for risk appetite: {risk}")
        return pd.DataFrame()

    result = filtered[["scheme_name", "risk_category",
                        "sharpe_ratio", "expense_ratio_pct", "fund_house"]]
    return result


def main():
    print("\n" + "="*60)
    print("  Bluestock MF — Fund Recommender")
    print("="*60)

    for risk in ["Low", "Moderate", "High", "Very High"]:
        print(f"\n Risk Appetite: {risk}")
        print("-"*60)
        result = recommend_funds(risk)
        if not result.empty:
            print(result.to_string(index=False))

if __name__ == "__main__":
    main()