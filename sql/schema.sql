-- Bluestock MF Capstone — Database Schema
-- Day 2: Star Schema Design

-- Dimension Table: Funds
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code         INTEGER PRIMARY KEY,
    fund_house        TEXT,
    scheme_name       TEXT,
    category          TEXT,
    sub_category      TEXT,
    plan              TEXT,
    benchmark         TEXT,
    expense_ratio_pct REAL,
    exit_load_pct     REAL,
    fund_manager      TEXT,
    risk_category     TEXT
);

-- Dimension Table: Dates
CREATE TABLE IF NOT EXISTS dim_date (
    date_id    TEXT PRIMARY KEY,
    year       INTEGER,
    month      INTEGER,
    quarter    INTEGER,
    is_weekday INTEGER
);

-- Fact Table: NAV History
CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code       INTEGER,
    date            TEXT,
    nav             REAL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact Table: Investor Transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    tx_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id        TEXT,
    amfi_code          INTEGER,
    transaction_date   TEXT,
    transaction_type   TEXT,
    amount_inr         INTEGER,
    state              TEXT,
    city               TEXT,
    city_tier          TEXT,
    age_group          TEXT,
    gender             TEXT,
    annual_income_lakh REAL,
    payment_mode       TEXT,
    kyc_status         TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact Table: Fund Performance
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code         INTEGER PRIMARY KEY,
    return_1yr_pct    REAL,
    return_3yr_pct    REAL,
    return_5yr_pct    REAL,
    sharpe_ratio      REAL,
    sortino_ratio     REAL,
    alpha             REAL,
    beta              REAL,
    max_drawdown_pct  REAL,
    std_dev_ann_pct   REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact Table: AUM by Fund House
CREATE TABLE IF NOT EXISTS fact_aum (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    date       TEXT,
    fund_house TEXT,
    aum_crore  INTEGER,
    num_schemes INTEGER
);