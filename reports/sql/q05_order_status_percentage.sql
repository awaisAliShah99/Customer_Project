-- Q5: What percentage of orders are completed, pending, cancelled, and returned?
SELECT
    order_status,
    COUNT(*)                                                         AS total_orders,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM customer_orders), 2) AS percentage
FROM customer_orders
GROUP BY order_status
ORDER BY total_orders DESC;