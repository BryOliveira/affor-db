-- TODO: document
-- make sure NOT NULL and UNIQUE constraints are in place
-- If an index is poorly chosen and clearly not tested, you will not receive full credit

-- Clean up tables if they already exist.
DROP TABLE IF EXISTS mortgage_rates;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS home_prices;

-- Clean up views
DROP VIEW IF EXISTS top_annual_salary_per_state;
DROP VIEW IF EXISTS top_annual_salary_per_sector;


-- Table containing the states and their median house prices.
CREATE TABLE home_prices (
    loc_state               CHAR(2) PRIMARY KEY,
    median_house_price      DECIMAL(12, 2) NOT NULL
);

-- Companies Table
CREATE TABLE companies (
    company_id              INT AUTO_INCREMENT PRIMARY KEY,
    company_name            VARCHAR(100),
    sector                  VARCHAR(100),
    loc_state               CHAR(2) NOT NULL,
    
    FOREIGN KEY (loc_state) REFERENCES home_prices(loc_state)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);



-- Jobs Table 
CREATE TABLE jobs (
    job_id                  INT AUTO_INCREMENT PRIMARY KEY,
    company_id              INT NOT NULL,
    job_title               VARCHAR(100) NOT NULL,
    job_description         TEXT,
    loc_city                VARCHAR(100),
    loc_state               CHAR(2) NOT NULL,
    min_salary              DECIMAL(10, 2),
    max_salary              DECIMAL(10, 2),
    avg_salary              DECIMAL(10, 2),
    is_hourly               BOOLEAN NOT NULL,

    FOREIGN KEY (company_id) REFERENCES companies(company_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE mortgage_rates (
    mortgage_id            INT AUTO_INCREMENT PRIMARY KEY,
    loc_city               VARCHAR(50),
    loc_state              CHAR(2) NOT NULL,
    date_recorded          DATE NOT NULL,
    rate_5                 DECIMAL(20, 10) NOT NULL,
    rate_10                DECIMAL(20, 10) NOT NULL, 
    rate_20                DECIMAL(20, 10) NOT NULL
);


-- indices to speed up queries
CREATE INDEX idx_jobs_loc_state_loc_city ON jobs(loc_state, loc_city);
CREATE INDEX idx_mortgage_rates_loc_state_loc_city_date ON mortgage_rates(loc_state, loc_city, date_recorded);



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