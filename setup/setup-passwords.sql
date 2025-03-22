-- from A6

DROP FUNCTION IF EXISTS make_salt;
DROP PROCEDURE IF EXISTS sp_add_user;
DROP FUNCTION IF EXISTS authenticate;
DROP PROCEDURE IF EXISTS sp_change_password;
DROP TABLE IF EXISTS user_info;

DELIMITER !

CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    SET num_chars = LEAST(20, num_chars);

    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !

DELIMITER ;

CREATE TABLE user_info (
    username VARCHAR(20) PRIMARY KEY,
    salt CHAR(8) NOT NULL,
    password_hash BINARY(64) NOT NULL
);

DELIMITER !

CREATE PROCEDURE sp_add_user(
    new_username VARCHAR(20),
    password VARCHAR(20)
)
BEGIN
    DECLARE salt_gen CHAR(8);
    DECLARE hashed_pass BINARY(64);

    SET salt_gen = make_salt(8);
    SET hashed_pass = SHA2(CONCAT(salt_gen, password), 256);

    INSERT INTO user_info (username, salt, password_hash)
    VALUES (new_username, salt_gen, hashed_pass);
END !

DELIMITER ;

DELIMITER !

CREATE FUNCTION authenticate(
    username VARCHAR(20),
    password VARCHAR(20)
)
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE stored_salt CHAR(8);
    DECLARE stored_hash BINARY(64);
    DECLARE computed_hash BINARY(64);

    IF NOT EXISTS (SELECT 1 FROM user_info WHERE username = username) THEN
        RETURN 0;
    END IF;

    SELECT salt, password_hash
    INTO stored_salt, stored_hash
    FROM user_info
    WHERE username = username;

    SET computed_hash = SHA2(CONCAT(stored_salt, password), 256);

    IF stored_hash = computed_hash THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END !

DELIMITER ;

DELIMITER !

CREATE PROCEDURE sp_change_password(
    username VARCHAR(20),
    new_password VARCHAR(20)
)
BEGIN
    DECLARE salt_gen CHAR(8);
    DECLARE hashed_pass BINARY(64);

    SET salt_gen = make_salt(8);
    SET hashed_pass = SHA2(CONCAT(salt_gen, new_password), 256);

    UPDATE user_info
    SET salt = salt_gen,
        password_hash = hashed_pass
    WHERE username = username;
END !

DELIMITER ;

-- default administrator
CALL sp_add_user('admin', 'admin');