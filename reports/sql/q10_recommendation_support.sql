-- Q10: Recommendations ke liye supporting data: har order status ki revenue mein hissedari.
-- Cancelled + Returned revenue = woh revenue jo haasil nahi hui.
SELECT
    order_status,
    COUNT(*)                                                         AS total_orders,
    ROUND(SUM(total_amount_pkr), 2)                                  AS revenue_pkr,
    ROUND(100 * SUM(total_amount_pkr)
          / (SELECT SUM(total_amount_pkr) FROM customer_orders), 2)  AS revenue_share_pct
FROM customer_orders
GROUP BY order_status
ORDER BY revenue_pkr DESC;