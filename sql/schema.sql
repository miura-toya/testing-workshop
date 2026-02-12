CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    plan VARCHAR(50) NOT NULL,
    months INT NOT NULL,
    monthly_price INT NOT NULL,
    discount_rate INT NOT NULL,
    total_price INT NOT NULL
);
