-- Q3: What is the average order value for each customer segment?
SELECT
    customer_segment,
    COUNT(*)                          AS total_orders,
    ROUND(AVG(total_amount_pkr), 2)   AS avg_order_value_pkr
FROM customer_orders
GROUP BY customer_segment
ORDER BY avg_order_value_pkr DESC;