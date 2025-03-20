-- TODO: document


DROP FUNCTION IF EXISTS get_avg_payment_length;
DELIMITER !

-- Calculates the average payment length in months
-- based on avg_salary, house_price, monthly_payment,
-- savings_percent, and interest_rate.

CREATE FUNCTION get_avg_payment_length(
    avg_salary DECIMAL(10, 2)       
    house_price DECIMAL(10, 2),      
    monthly_payment DECIMAL(15, 10), 
    savings_percent DECIMAL(10, 2),  
    interest_rate DECIMAL(10, 2)     
) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE avg_payment_length INT DEFAULT 0; 
    DECLARE monthly_savings DECIMAL(12, 2);
    DECLARE monthly_interest_amount DECIMAL(12, 2);
    DECLARE total_payment DECIMAL(12, 2);

    SET monthly_savings = (avg_salary / 12) * (savings_percent / 100);

    IF (monthly_payment + monthly_savings) <= (house_price * interest_rate / 100) THEN
        RETURN -1; 
    END IF;

    WHILE house_price > 0 DO
        SET house_price = house_price + (house_price * interest_rate / 100);

        SET total_payment = monthly_payment + monthly_savings;
        SET house_price = house_price - total_payment;

        SET avg_payment_length = avg_payment_length + 1;

        IF avg_payment_length > 12 * 31 THEN
            RETURN -1; 
        END IF;
    END WHILE;

    RETURN avg_payment_length;
END !

DELIMITER ;


DROP FUNCTION IF EXISTS calc_monthly_mortgage_payment;
DELIMITER !

-- Calculates the monthly mortgage payment
-- based on house_price, down_payment_percent (user)
-- and annual_interest_rate (user) and loan_term_years (user).

CREATE FUNCTION calc_monthly_mortgage_payment(
    house_price DECIMAL(12, 2),
    down_payment_percent DECIMAL(5, 2), 
    annual_interest_rate DECIMAL(5, 2), 
    loan_term_years INT
) RETURNS DECIMAL(12, 2)
DETERMINISTIC
BEGIN
    DECLARE loan_amount DECIMAL(12, 2);
    DECLARE monthly_interest_rate DECIMAL(12, 6);
    DECLARE num_payments INT;
    DECLARE monthly_payment DECIMAL(12, 2);

    SET loan_amount = house_price * (1 - down_payment_percent / 100);
    SET monthly_interest_rate = annual_interest_rate / 100 / 12;
    SET num_payments = loan_term_years * 12;

    IF monthly_interest_rate = 0 THEN
        SET monthly_payment = loan_amount / num_payments;
    ELSE
        SET monthly_payment = loan_amount * 
            (monthly_interest_rate * POW(1 + monthly_interest_rate, num_payments)) /
            (POW(1 + monthly_interest_rate, num_payments) - 1);
    END IF;

    RETURN monthly_payment;
END !

DELIMITER ;

DROP PROCEDURE IF EXISTS add_job_listing;
DELIMITER !


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

DELIMITER ;

DROP TRIGGER IF EXISTS update_avg_salary_before_insert;
DELIMITER !


-- Trigger to calculate avg_salary before inserting a new job listing
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


