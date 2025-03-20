LOAD DATA LOCAL INFILE 'data/home_prices.csv'
INTO TABLE home_prices
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(loc_state, median_house_price);

LOAD DATA LOCAL INFILE 'data/companies.csv'
INTO TABLE companies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(company_id,company_name,sector,loc_state);

LOAD DATA LOCAL INFILE 'data/jobs.csv'
INTO TABLE jobs
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(company_id, job_title, job_description, loc_city, loc_state, min_salary, max_salary, avg_salary, is_hourly);

LOAD DATA LOCAL INFILE 'data/mortgage_payments.csv'
INTO TABLE mortgage_rates
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(loc_city, loc_state, date_recorded, rate_5, rate_10, rate_20);
