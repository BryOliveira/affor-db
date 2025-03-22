-- Clean up views if they already exist.
-- GIVES warnings when the views dont exist
-- which is fine.
DROP VIEW IF EXISTS latest_mortgage_rates;
DROP VIEW IF EXISTS v_jobs_with_annual_salary;
DROP VIEW IF EXISTS top_annual_salary_per_sector;
DROP VIEW IF EXISTS top_annual_salary_per_state;

-- Clean up tables if they already exist.
DROP TABLE IF EXISTS mortgage_rates;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS home_prices;

-- Table containing the states and their median house prices.
CREATE TABLE home_prices (
    loc_state               CHAR(2) PRIMARY KEY,
    median_house_price      DECIMAL(12, 2) NOT NULL
);

-- Companies Table: Stores company information including sector and location
CREATE TABLE companies (
    company_id              INT AUTO_INCREMENT PRIMARY KEY,
    company_name            VARCHAR(100) NOT NULL,
    sector                  VARCHAR(100) NOT NULL,
    loc_state               CHAR(2) NOT NULL,
    
    FOREIGN KEY (loc_state) REFERENCES home_prices(loc_state)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Jobs Table: Contains job listings with salary information and location details
CREATE TABLE jobs (
    job_id                  INT AUTO_INCREMENT PRIMARY KEY,
    company_id              INT NOT NULL,
    job_title               VARCHAR(100) NOT NULL,
    job_description         TEXT,
    loc_city                VARCHAR(100),
    loc_state               CHAR(2) NOT NULL,
    min_salary              DECIMAL(10, 2) CHECK (min_salary > 0),
    max_salary              DECIMAL(10, 2) CHECK (max_salary > 0),
    avg_salary              DECIMAL(10, 2),
    is_hourly               BOOLEAN NOT NULL,

    FOREIGN KEY (company_id) REFERENCES companies(company_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT salary_range CHECK (max_salary >= min_salary),
    CONSTRAINT valid_avg_salary CHECK (avg_salary BETWEEN min_salary AND max_salary)
);

-- Mortgage rates table: Tracks interest rates by state, term length and date
CREATE TABLE mortgage_rates (
    loc_state CHAR(2),
    loan_term_years INT NOT NULL CHECK (loan_term_years IN (10,15,30)),
    date_recorded DATE NOT NULL,
    annual_interest_rate DECIMAL(5, 2) NOT NULL CHECK (annual_interest_rate BETWEEN 0 AND 100),

    PRIMARY KEY (loc_state, loan_term_years, date_recorded),

    FOREIGN KEY (loc_state) REFERENCES home_prices(loc_state)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- index to speed up queries
CREATE INDEX idx_jobs_state_city ON jobs(loc_state, loc_city);

-- Creates a view to show the top annual salary for each state.
CREATE VIEW top_annual_salary_per_state AS
SELECT
    loc_state,
    MAX(
        CASE
            WHEN is_hourly = 0 THEN avg_salary * 1000
            WHEN is_hourly = 1 THEN avg_salary * 40 * 52
        END
    ) AS max_annual_salary
FROM jobs
GROUP BY loc_state;

-- Creates a view to show the top annual salary for each sector.
CREATE VIEW top_annual_salary_per_sector AS
SELECT
    sector,
    MAX(
        CASE
            WHEN is_hourly = 0 THEN avg_salary * 1000
            WHEN is_hourly = 1 THEN avg_salary * 40 * 52
        END
    ) AS max_annual_salary
FROM jobs
JOIN companies ON jobs.company_id = companies.company_id
WHERE sector != '-1'
GROUP BY sector ORDER BY max_annual_salary DESC;

-- Creates a view with annualized salary for each job.
-- the data within the table is
-- either hourly or annual, it makes more sense to standardize
-- it.

CREATE VIEW v_jobs_with_annual_salary AS
SELECT
    j.job_id,
    j.job_title,
    j.job_description,
    j.loc_city,
    j.loc_state,
    CASE
        WHEN j.is_hourly = 1 THEN ROUND(j.min_salary * 40 * 52, 2)
        ELSE j.min_salary
    END AS min_salary,
    CASE
        WHEN j.is_hourly = 1 THEN ROUND(j.max_salary * 40 * 52, 2)
        ELSE j.max_salary
    END AS max_salary,
    CASE
        WHEN j.is_hourly = 1 THEN ROUND(j.avg_salary * 40 * 52, 2)
        ELSE j.avg_salary
    END AS avg_salary,
    j.is_hourly,
    c.company_name,
    CASE
        WHEN j.is_hourly = 1 THEN ROUND(j.avg_salary * 40 * 52, 2)
        ELSE j.avg_salary
    END AS annualized_salary
FROM jobs j
JOIN companies c ON j.company_id = c.company_id;


CREATE VIEW latest_mortgage_rates AS
SELECT loc_state, loan_term_years, date_recorded, annual_interest_rate
FROM mortgage_rates
WHERE (loc_state, loan_term_years, date_recorded) IN (
    SELECT loc_state, loan_term_years, MAX(date_recorded)
    FROM mortgage_rates
    GROUP BY loc_state, loan_term_years
);
