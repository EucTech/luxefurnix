-- This is st up for luxefurnix DATABASE

CREATE DATABASE IF NOT EXISTS luxefurnix_db;
CREATE USER IF NOT EXISTS 'luxefurnix'@'localhost' IDENTIFIED BY 'luxefurnix_pwd';
GRANT ALL PRIVILEGES ON `luxefurnix_db`.* TO 'luxefurnix'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'luxefurnix'@'localhost';
FLUSH PRIVILEGES;