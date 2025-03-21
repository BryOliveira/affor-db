-- Retrieves job details for a given job ID
-- note that salary is either hourly or annual
-- annual is in units of thousands
-- and hourly is in units of dollars 
SELECT 
    j.job_id, 
    j.job_title, 
    c.company_name, 
    j.loc_city, 
    j.loc_state, 
    j.min_salary, 
    j.max_salary,
    j.is_hourly
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
WHERE j.job_id = 123;

-- Retrieves median house price for a specific state (e.g., 'CA')
-- note that the median house price is in THOUSANDS of dollars
SELECT median_house_price
FROM home_prices
WHERE loc_state = 'CA';

-- aggregates the average salary for each job title that appears more
-- than once in the jobs table (top 10)
-- RA

SELECT job_title, ROUND(AVG(avg_salary)*1000,2) AS avg_salary
FROM v_jobs_with_annual_salary
GROUP BY job_title
HAVING COUNT(*) > 1
ORDER BY avg_salary DESC
LIMIT 10;



-- Calculates monthly mortgage payment (example parameters)
-- note this is a function call
SELECT calc_monthly_mortgage_payment(500000, 20, 'CA', 30) AS monthly_payment;

-- Calculates affordability of buying home for Engineering jobs across FL, CA, and NY
-- Joins jobs with mortgage rates for a 30-year loan using the latest available rate.
SELECT 
    j.loc_state,
    j.job_title,
    j.avg_salary, 
    calc_monthly_mortgage_payment(hp.median_house_price, 20, j.loc_state, 30) AS monthly_mortgage_payment,
    calc_affordability_ratio(
        j.avg_salary * 1000,
        calc_monthly_mortgage_payment(hp.median_house_price, 20, j.loc_state, 30)
    ) AS affordability_ratio
FROM v_jobs_with_annual_salary j
JOIN latest_mortgage_rates mr ON j.loc_state = mr.loc_state AND mr.loan_term_years = 30
JOIN home_prices hp ON j.loc_state = hp.loc_state
WHERE j.job_title LIKE '%Engineer%'
  AND j.loc_state IN ('FL', 'CA', 'NY')
ORDER BY j.loc_state;

-- top annual salaries grouped by state
-- RA
SELECT 
    c.sector,
    MAX(CASE WHEN j.is_hourly = 1 THEN j.avg_salary * 40 * 52 ELSE j.avg_salary * 1000 END) AS max_annual_salary
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
GROUP BY c.sector
ORDER BY max_annual_salary DESC;


-- top annual salaries grouped by sector
-- invokes top_annual_salary_per_sector
SELECT sector, max_annual_salary
FROM top_annual_salary_per_sector
ORDER BY max_annual_salary DESC;

-- gets job listings by job title, city, and state with salary range, ordered by salary
-- finding analyst positions in San Francisco
-- and returns the top 10 job titles with the highest average salary
-- RA 
SELECT job_id, job_title, company_name, loc_city, loc_state, min_salary, max_salary, avg_salary
FROM v_jobs_with_annual_salary
WHERE job_title LIKE '%Analyst%'
  AND LOWER(loc_city) LIKE '%san francisco%'
  AND loc_state = 'CA'
  AND min_salary >= 50
  AND max_salary <= 250
ORDER BY avg_salary DESC
LIMIT 10;

-- Inserts a new mortgage rate (RIP)
INSERT INTO mortgage_rates (loc_state, loan_term_years, date_recorded, annual_interest_rate)
VALUES ('CA', 30, '2024-03-01', 10.5);

-- Updates median house price for a given state 
UPDATE home_prices
SET median_house_price = 750000
WHERE loc_state = 'CA';

-- Deletes a job by job_id 
DELETE FROM jobs
WHERE job_id = 373;
