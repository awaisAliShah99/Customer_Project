-- Q1: Which cities generate the highest number of orders and total revenue?
-- total_revenue = saare orders ki value; completed_revenue = sirf Completed orders.
SELECT
    city,
    COUNT(*)                                                        AS total_orders,
    ROUND(SUM(total_amount_pkr), 2)                                 AS total_revenue_pkr,
    ROUND(SUM(CASE WHEN order_status = 'Completed'
                   THEN total_amount_pkr ELSE 0 END), 2)            AS completed_revenue_pkr
FROM customer_orders
GROUP BY city
ORDER BY total_orders DESC, total_revenue_pkr DESC;