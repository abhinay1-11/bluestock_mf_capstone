-- Bluestock MF Capstone — Analytical Queries
-- Day 2: 10 SQL Queries

-- Q1: Top 5 funds by AUM
SELECT fund_house, SUM(aum_crore) as total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;

-- Q2: Average NAV per month for each fund
SELECT amfi_code,
       strftime('%Y-%m', date) as month,
       ROUND(AVG(nav), 2) as avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- Q3: SIP inflow YoY growth
SELECT strftime('%Y', month) as year,
       SUM(sip_inflow_crore) as total_sip
FROM fact_sip_industry
GROUP BY year
ORDER BY year;

-- Q4: Total transactions by state
SELECT state,
       COUNT(*) as total_transactions,
       SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- Q5: Funds with expense ratio less than 1%
SELECT amfi_code, fund_house, scheme_name, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Q6: Top 5 funds by Sharpe ratio
SELECT amfi_code, sharpe_ratio, return_3yr_pct
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 5;

-- Q7: Transaction split by type
SELECT transaction_type,
       COUNT(*) as count,
       SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY transaction_type;

-- Q8: Average SIP amount by age group
SELECT age_group,
       ROUND(AVG(amount_inr), 2) as avg_amount,
       COUNT(*) as total_transactions
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY age_group
ORDER BY avg_amount DESC;

-- Q9: Top 5 funds by 3 year return
SELECT amfi_code, return_3yr_pct, sharpe_ratio, alpha
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- Q10: Funds with negative alpha (underperforming benchmark)
SELECT amfi_code, alpha, beta, return_3yr_pct
FROM fact_performance
WHERE alpha < 0
ORDER BY alpha ASC;