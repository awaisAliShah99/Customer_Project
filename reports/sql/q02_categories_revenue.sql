-- Q2: Which product categories generate the most revenue?
SELECT
    product_category,
    COUNT(*)                                                        AS total_orders,
    ROUND(SUM(total_amount_pkr), 2)                                 AS total_revenue_pkr,
    ROUND(100 * SUM(total_amount_pkr)
          / (SELECT SUM(total_amount_pkr) FROM customer_orders), 2) AS revenue_share_pct
FROM customer_orders
GROUP BY product_category
ORDER BY total_revenue_pkr DESC;