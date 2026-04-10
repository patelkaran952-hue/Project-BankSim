SET GLOBAL local_infile = 1;

SHOW VARIABLES LIKE 'local_infile';

SHOW VARIABLES LIKE 'secure_file_priv';

-- Creating table

CREATE TABLE transactions_raw (
    step INT,
    customer VARCHAR(50),
    age VARCHAR(10),
    gender VARCHAR(10),
    zipcodeOri INT,
    merchant VARCHAR(50),
    zipMerchant INT,
    category VARCHAR(50),
    amount FLOAT,
    fraud INT
);

-- Loading raw data into the table

LOAD DATA LOCAL INFILE "C:/Program Files/MySQL/MySQL Server 8.0/Uploads/bs140513_032310.csv"
INTO TABLE transactions_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

select * from transactions_raw LIMIT 10;

-- Creating a copy of main table

create table transactions
like transactions_raw;

insert transactions
select *
from transactions_raw;

-- DATA CLEANING

-- Dropping unnecessary columns

alter table transactions
drop zipcodeOri;

alter table transactions
drop zipMerchant;


select distinct customer from transactions;    -- There are total 4112 unique customers in this dataset

select distinct merchant from transactions;    -- There are total 50 unique merchants in this dataset

select * from transactions where fraud = 1 ;   -- There are total 7200 frauds transactions 

update transactions
set amount = trim(amount);

select * from transactions limit 5; 


-- Checking duplicate values

SELECT *,
ROW_NUMBER() OVER (
    PARTITION BY customer, step, amount, merchant, category
) AS rn
FROM transactions;

SELECT *
FROM (
    SELECT *,
    ROW_NUMBER() OVER (
        PARTITION BY customer, step, amount, merchant, category
    ) AS rn
    FROM transactions
) t
WHERE rn > 1;            -- There are no duplicate values


-- Avg transaction amount (fraud vs non-fraud)

SELECT fraud, AVG(amount)
FROM transactions
GROUP BY fraud;


-- Handling unknown values

SELECT COUNT(*) 
FROM transactions 
WHERE age = 'U';

SELECT age, count(fraud)
FROM transactions
WHERE fraud = 1
GROUP BY age;

update transactions
set age = trim(age);


select distinct amount from transactions;

update transactions
set amount = trim(amount);


SELECT MIN(amount), MAX(amount), AVG(amount)
FROM transactions;

select * from transactions
where amount >= 500 
order by amount asc;

select avg(amount) from transactions     -- Average fraud transaction amount is 530.92
where fraud = 0;                         -- Average fair transaction amount is 31.84


-- Fraud transactions per category

SELECT DISTINCT category FROM transactions;

select category, count(fraud) as fraud_transactions from transactions
where fraud = 1
group by category
order by fraud_transactions desc;                     -- The most fraud transactions are in sports and toys category - 1982

SELECT * 
FROM transactions
WHERE category LIKE '%sportsandtoys%';

select category, avg(amount) from transactions
where category like '%sportsandtoys%' and fraud = 1
group by category;

select category, avg(amount) from transactions
where category like '%health%' and fraud = 1
group by category;

select category, avg(amount) from transactions
where category like '%wellnessandbeauty%' and fraud = 1
group by category;


-- Creating new column for high and low amount transactions

select avg(amount) from transactions;

SELECT *,
CASE 
  WHEN amount > 200 THEN 'High'
  WHEN amount > 1000 THEN 'Very High'
  ELSE 'Low'
END AS amount_category
FROM transactions;

select min(amount) from transactions where fraud = 1;


-- Removing unnecessary rows

delete from transactions where amount = 0;

select * from transactions limit 10;

SELECT category, COUNT(*) 
FROM transactions 
GROUP BY category;


-- Finding fraud patterns

select age, count(fraud) from transactions
where fraud = 1
group by age
order by count(fraud) desc;             -- age 2(25-35) customers are on the top of the list of fraud transactions followed by age 3(35-45) and age 4(45-55)

select step, count(fraud) from transactions
where fraud = 1
group by step
order by count(fraud) desc;             -- There are exactly 40 fraud transactions on each and every step(day)


select gender, count(fraud) from transactions
where fraud = 1
group by gender
order by count(fraud) desc;              -- Fraud transactions by female - 4758
										 -- Fraud transactions by male - 2435


select customer, gender, age, count(fraud) from transactions
where fraud = 1
group by customer, gender, age
order by count(fraud) desc;               -- There are total 1483 customers with fraud transaction. Top 10 customers with most fraud transactions are Female.


select * from transactions 
where customer like '%C1350963410%' and fraud = 1;

select customer, category, amount, fraud from transactions
where customer like '%C366397964%' and fraud = 1
order by amount desc;

select sum(amount) from transactions
where fraud = 1;                           -- Total amount of all the fraud transactions - 3822671.17

select step, sum(amount) from transactions
where fraud = 1
group by step
order by sum(amount) desc;

select category, count(fraud) as fraud_transactions, age from transactions
where fraud = 1
group by category, age
order by fraud_transactions desc;   

select customer, max(amount), age, category from transactions
where fraud = 1
group by age, category, customer
order by max(amount) desc;

SELECT category, 
       SUM(amount) AS total_fraud_amount, 
       COUNT(fraud) AS fraud_count
FROM transactions
WHERE fraud = 1
GROUP BY category
ORDER BY total_fraud_amount DESC;

SELECT 
    category,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN fraud = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
    SUM(CASE WHEN fraud = 1 THEN amount ELSE 0 END) AS total_fraud_amount
FROM transactions
GROUP BY category;



