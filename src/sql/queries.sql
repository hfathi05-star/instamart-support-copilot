
-- Q1: WHERE and HAVING
SELECT
    customer_id,
    SUM(order_amount) AS total_spend
FROM orders
WHERE status = 'completed'
  AND order_amount > 500
GROUP BY customer_id
HAVING SUM(order_amount) > 8000;



-- Q2: Revenue by city and product category
SELECT
    c.city,
    p.category,
    SUM(o.order_amount) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.city, p.category
ORDER BY c.city, p.category;
-- Q3: Products priced above average catalogue price
SELECT *
FROM products
WHERE price_inr > (
    SELECT AVG(price_inr)
    FROM products
);
-- Q4: LEFT JOIN - Customers with no completed orders

SELECT c.customer_id
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
    AND o.status = 'completed'
WHERE o.order_id IS NULL;
-- Q5: CTE - Customers spending above average

WITH customer_spend AS (
    SELECT
        customer_id,
        SUM(order_amount) AS total_spend
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
average_spend AS (
    SELECT AVG(total_spend) AS avg_spend
    FROM customer_spend
)
SELECT cs.customer_id, cs.total_spend
FROM customer_spend cs
CROSS JOIN average_spend a
WHERE cs.total_spend > a.avg_spend;
-- Q6: Ranking Window Functions

SELECT
    city,
    customer_id,
    total_spend,
    RANK() OVER (
        PARTITION BY city
        ORDER BY total_spend DESC
    ) AS rank_no,
    DENSE_RANK() OVER (
        PARTITION BY city
        ORDER BY total_spend DESC
    ) AS dense_rank_no,
    ROW_NUMBER() OVER (
        PARTITION BY city
        ORDER BY total_spend DESC
    ) AS row_no
FROM (
    SELECT
        c.city,
        o.customer_id,
        SUM(o.order_amount) AS total_spend
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.city, o.customer_id
);
-- Q7: Running Total of Daily Revenue

SELECT
    substr(order_ts, 1, 10) AS day,
    SUM(order_amount) AS daily_revenue,
    SUM(SUM(order_amount)) OVER (
        ORDER BY substr(order_ts, 1, 10)
    ) AS cumulative_revenue
FROM orders
WHERE status = 'completed'
GROUP BY substr(order_ts, 1, 10)
ORDER BY day;