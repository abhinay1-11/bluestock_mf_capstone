# Bluestock MF Capstone — Data Dictionary

## 01_fund_master.csv
| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER | Unique AMFI scheme code |
| fund_house | TEXT | AMC name (e.g. SBI Mutual Fund) |
| scheme_name | TEXT | Full official scheme name |
| category | TEXT | Equity / Debt |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap etc. |
| plan | TEXT | Regular or Direct |
| benchmark | TEXT | Official benchmark index |
| expense_ratio_pct | REAL | Annual expense ratio in % |
| exit_load_pct | REAL | Exit load percentage |
| fund_manager | TEXT | Primary fund manager name |
| risk_category | TEXT | Low / Moderate / High / Very High |

## 02_nav_history.csv
| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER | Foreign key to fund_master |
| date | DATE | NAV date (business days only) |
| nav | REAL | Net Asset Value in Rs. |

## 07_scheme_performance.csv
| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER | Foreign key to fund_master |
| return_1yr_pct | REAL | 1 year absolute return % |
| return_3yr_pct | REAL | 3 year CAGR % |
| return_5yr_pct | REAL | 5 year CAGR % |
| sharpe_ratio | REAL | Risk adjusted return (higher is better) |
| sortino_ratio | REAL | Like Sharpe but penalises only downside |
| alpha | REAL | Return above benchmark |
| beta | REAL | Sensitivity to market movements |
| max_drawdown_pct | REAL | Worst peak to trough decline |

## 08_investor_transactions.csv
| Column | Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | DATE | Date of transaction |
| amfi_code | INTEGER | Fund in which transaction occurred |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount in rupees |
| state | TEXT | Investor state |
| city_tier | TEXT | T30 or B30 city classification |
| age_group | TEXT | 18-25 / 26-35 / 36-45 / 46-55 / 56+ |
| gender | TEXT | Male / Female |
| kyc_status | TEXT | Verified / Pending |