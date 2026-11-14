-- Q6: Which months have the highest and lowest sales?
-- Sabse upar = highest, sabse neeche = lowest. Aakhri month (2026-10) adhura ho sakta hai.
SELECT
    DATE_FORMAT(order_date, '%Y-%m')  AS order_month,
    COUNT(*)                          AS total_orders,
    ROUND(SUM(total_amount_pkr), 2)   AS total_sales_pkr
FROM customer_orders
GROUP BY order_month
ORDER BY total_sales_pkr DESC;