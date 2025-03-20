DROP FUNCTION IF EXISTS get_avg_payment_length;
DELIMITER !
CREATE FUNCTION get_avg_payment_length(
    avg_salary DECIMAL(10, 2),
    house_price DECIMAL(10, 2),
    monthly_payment DECIMAL(15, 10),
    savings_percent DECIMAL(10, 2),
    interest_rate DECIMAL(10, 2)
) RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE avg_payment_length DECIMAL(10, 2);
    DECLARE monthly_savings DECIMAL(10, 2);

    SET monthly_savings = (avg_salary * savings_percent) / 100;
    SET avg_payment_length = 0;

    WHILE house_price > 0 DO
        SET house_price = house_price - (monthly_payment + monthly_savings);
        SET avg_payment_length = avg_payment_length + 1;
        SET monthly_payment = monthly_payment + (monthly_payment * interest_rate / 100);
    END WHILE;

    RETURN avg_payment_length;


END !
DELIMITER ;


-- procedure to get
-- years to pay off house
-- salary savings (adjusted)

DROP PROCEDURE IF EXISTS get_years_to_pay_off_house;
DELIMITER !
