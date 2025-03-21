DROP USER IF EXISTS 'appadmin'@'localhost';
DROP USER IF EXISTS 'appclient'@'localhost';

CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'adminpw';

CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'clientpw';

GRANT ALL PRIVILEGES ON affordb.* TO 'appadmin'@'localhost';

GRANT SELECT ON affordb.* TO 'appclient'@'localhost';

FLUSH PRIVILEGES;