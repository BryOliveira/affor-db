-- Clean up tables if they already exist.
DROP TABLE IF EXISTS affordability_calculations;
DROP TABLE IF EXISTS mortgage_rates;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS companies;

-- Table containing the states and median house prices
CREATE TABLE locations (
    loc_state                   VARCHAR(50) PRIMARY KEY,
    median_house_price          DECIMAL(12, 2) NOT NULL
);

-- Table containing companies
CREATE TABLE companies (
    company_id                  INT AUTO_INCREMENT PRIMARY KEY,
    company_name                VARCHAR(100) NOT NULL,
    loc_state                   VARCHAR(50) NOT NULL REFERENCES locations,
    industry                    VARCHAR(100)
);

-- Table containing job postings
CREATE TABLE jobs (
    job_id                      INT AUTO_INCREMENT PRIMARY KEY,
    company_id                  INT NOT NULL REFERENCES companies,
    job_title                   VARCHAR(100) NOT NULL,
    job_description             TEXT,
    loc_state                   VARCHAR(50) NOT NULL REFERENCES locations,
    min_salary                  DECIMAL(10, 2),
    max_salary                  DECIMAL(10, 2),
    salary_type                 VARCHAR(10) NOT NULL, -- Hourly or Annual Pay
    posted_date                 DATE DEFAULT 'CURRENT_DATE'
);

-- Table containing average mortgage rates based on location
-- also has average monthly mortgage payment based on rates
-- based on percentage of down payment.
CREATE TABLE mortgage_rates (
    mortgage_id                 INT AUTO_INCREMENT PRIMARY KEY,
    loc_state                   VARCHAR(50) REFERENCES locations,
    avg_payment_20              DECIMAL(12, 2) NOT NULL, -- Payment 20% down
    avg_payment_10              DECIMAL(12, 2) NOT NULL, -- Payment 10% down
    avg_payment_5               DECIMAL(12, 2) NOT NULL, -- Payment 5% down
    median_mortgage_rate        DECIMAL(5, 2) NOT NULL, -- Curr. rate for state
    last_updated                DATE DEFAULT 'CURRENT_DATE',
);

-- Originally a table, but needs to be something more temporary 
-- for the sake of tailoring the entries to the user query.
-- Maybe just make a python function to calculate and display the calculation

-- Table (maybe should be made a view) that
-- calculates the affordability of a state based on
-- the salary of job postings and the median mortgage costs.
-- CREATE TABLE affordability_calculations (
--     calc_id                     INT AUTO_INCREMENT PRIMARY KEY,
--     job_id                      INT NOT NULL REFERENCES jobs,
--     loc_state                   VARCHAR(50) NOT NULL REFERENCES locations,
--     mortgage_id                 INT NOT NULL REFERENCES mortgage_rates,
--     estimated_years_to_afford   DECIMAL(5, 2) NOT NULL,
--     last_updated                DATE DEFAULT 'CURRENT_DATE'
-- );

-- indices to speed up queries that we've thought up
-- SUBJECT TO CHANGE!!
CREATE INDEX idx_locations_loc_state ON locations (loc_state);
CREATE INDEX idx_jobs_loc_state_posted_date ON jobs(loc_state, posted_date);
CREATE INDEX idx_mortgage_rates_loc_state_median_rate ON mortgage_rates(loc_state, median_mortgage_rate);