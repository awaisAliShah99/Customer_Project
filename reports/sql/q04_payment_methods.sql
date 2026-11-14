-- Q4: Which payment methods are most frequently used?
SELECT
    payment_method,
    COUNT(*)                                                         AS total_orders,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM customer_orders), 2) AS share_pct
FROM customer_orders
GROUP BY payment_method
ORDER BY total_orders DESC;