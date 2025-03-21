-- Drop existing methods
DROP FUNCTION IF EXISTS get_avg_payment_length;
DROP PROCEDURE IF EXISTS add_job_listing;
DROP FUNCTION IF EXISTS calc_monthly_mortgage_payment;
DROP FUNCTION IF EXISTS calc_max_affordable_house_price;
DROP FUNCTION IF EXISTS get_latest_annual_interest_rate;
DROP FUNCTION IF EXISTS calc_affordability_ratio;
DROP TRIGGER IF EXISTS update_avg_salary_before_insert;


DELIMITER !

-- FUN to get latest from mortgage_rates table
CREATE FUNCTION get_latest_annual_interest_rate(
    in_loc_state CHAR(2),
    in_loan_term_years INT
) RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE latest_interest_rate DECIMAL(5,2);

    SELECT annual_interest_rate
    INTO latest_interest_rate
    FROM mortgage_rates
    WHERE loc_state = in_loc_state
      AND loan_term_years = in_loan_term_years
    ORDER BY date_recorded DESC
    LIMIT 1;

    RETURN latest_interest_rate;
END !

-- calc_monthly_mortgage_payment based on
-- house_price, down_payment_percent, annual_interest_rate, loan_term_years
CREATE FUNCTION calc_monthly_mortgage_payment(
    house_price DECIMAL(12, 2),
    down_payment_percent DECIMAL(5, 2),
    in_loc_state CHAR(2),               
    loan_term_years INT
) RETURNS DECIMAL(12, 2)
DETERMINISTIC
BEGIN
    DECLARE annual_interest_rate DECIMAL(5,2);
    DECLARE monthly_interest_rate DECIMAL(12, 6);
    DECLARE num_payments INT;
    DECLARE loan_amount DECIMAL(12, 2);
    DECLARE monthly_payment DECIMAL(12, 2);

    SET annual_interest_rate = get_latest_annual_interest_rate(in_loc_state, loan_term_years);

    SET monthly_interest_rate = annual_interest_rate / 100 / 12;
    SET num_payments = loan_term_years * 12;

    SET loan_amount = house_price * (1 - down_payment_percent / 100);

    IF monthly_interest_rate = 0 THEN
        SET monthly_payment = loan_amount / num_payments;
    ELSE
        SET monthly_payment = loan_amount *
            (monthly_interest_rate * POW(1 + monthly_interest_rate, num_payments)) /
            (POW(1 + monthly_interest_rate, num_payments) - 1);
    END IF;

    RETURN ROUND(monthly_payment, 2);
END;

-- calculate affordability ratio, which is
-- basically just the monthly mortgage payment
-- divided by the monthly income
CREATE FUNCTION calc_affordability_ratio(
    avg_salary DECIMAL(12, 2),     
    monthly_mortgage_payment DECIMAL(12, 2)
) RETURNS DECIMAL(5, 2)
DETERMINISTIC
BEGIN
    DECLARE monthly_income DECIMAL(12, 2);

    SET monthly_income = avg_salary / 12;

    IF monthly_mortgage_payment = 0 THEN
        RETURN NULL; 
    END IF;

    RETURN ROUND((monthly_mortgage_payment / monthly_income) * 100, 2); 
END !

-- Procedure to add a new job listing
-- takes in all the required fields
-- and inserts them into the jobs table.
CREATE PROCEDURE add_job_listing(
    IN in_company_id INT,
    IN in_job_title VARCHAR(100),
    IN in_job_description TEXT,
    IN in_city VARCHAR(100),
    IN in_loc_state CHAR(2),
    IN in_min_salary DECIMAL(10, 2),
    IN in_max_salary DECIMAL(10, 2),
    IN in_avg_salary DECIMAL(10, 2),
    IN in_is_hourly BOOLEAN
)
BEGIN
    INSERT INTO jobs (
        company_id,
        job_title,
        job_description,
        city,
        loc_state,
        min_salary,
        max_salary,
        avg_salary,
        is_hourly
    )
    VALUES (
        in_company_id,
        in_job_title,
        in_job_description,
        in_city,
        in_loc_state,
        in_min_salary,
        in_max_salary,
        in_avg_salary,
        in_is_hourly
    );
END !

-- Trigger to impute avg_salary before inserting a new job listing
-- if just a range is provided, and avg_salary is not provided.
CREATE TRIGGER update_avg_salary_before_insert
BEFORE INSERT ON jobs
FOR EACH ROW
BEGIN
    IF NEW.avg_salary IS NULL THEN
        IF NEW.min_salary IS NOT NULL AND NEW.max_salary IS NOT NULL THEN
            SET NEW.avg_salary = (NEW.min_salary + NEW.max_salary) / 2;
        END IF;
    END IF;
END !

DELIMITER ;