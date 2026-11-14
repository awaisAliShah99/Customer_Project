-- Q7: Which customers have spent the most money? (top 10)
SELECT
    customer_id,
    CONCAT(first_name, ' ', last_name)  AS customer_name,
    city,
    customer_segment,
    COUNT(*)                            AS total_orders,
    ROUND(SUM(total_amount_pkr), 2)     AS total_spent_pkr
FROM customer_orders
GROUP BY customer_id, first_name, last_name, city, customer_segment
ORDER BY total_spent_pkr DESC
LIMIT 10;