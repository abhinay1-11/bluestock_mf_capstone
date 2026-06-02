import pandas as pd
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR  = BASE_DIR / "data" / "raw"

SCHEMES = {
    125497: "HDFC_Top100_Direct",
    119551: "SBI_Bluechip_Direct",
    120503: "ICICI_Bluechip_Direct",
    118632: "Nippon_LargeCap_Direct",
    119092: "Axis_Bluechip_Direct",
    120841: "Kotak_Bluechip_Direct",
}

BASE_URL = "https://api.mfapi.in/mf/{scheme_code}"

def fetch_nav(scheme_code, scheme_name):
    url = BASE_URL.format(scheme_code=scheme_code)
    print(f"Fetching [{scheme_code}] {scheme_name} ...", end=" ")

    response = requests.get(url, timeout=15)
    payload = response.json()

    nav_records = payload.get("data", [])
    meta = payload.get("meta", {})

    df = pd.DataFrame(nav_records)
    df["scheme_code"] = scheme_code
    df["scheme_name"] = meta.get("scheme_name", scheme_name)

    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"]  = pd.to_numeric(df["nav"])
    df.sort_values("date", inplace=True)

    print(f"OK — {len(df)} records")
    return df

def save_raw(df, scheme_name):
    out_path = RAW_DIR / f"nav_{scheme_name}.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved → {out_path.name}")

for code, name in SCHEMES.items():
    df = fetch_nav(code, name)
    save_raw(df, name)

print("\nAll NAV files fetched and saved!")