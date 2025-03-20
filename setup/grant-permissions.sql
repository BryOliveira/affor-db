CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON affordb.* TO 'appadmin'@'localhost';
FLUSH PRIVELEGES;