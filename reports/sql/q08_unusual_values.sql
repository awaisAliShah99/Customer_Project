-- Q8: Are there unusual prices, quantities, or order totals that require investigation?
-- Har measure ke liye range, average, std dev, aur kitne records average + 2 std dev se upar hain.
-- Note: extreme outliers (qty 999, price 9,999,999, total 99,999,999, negatives) validation mein
-- pehle hi reject/correct ho chuke hain (dekho Q9), isliye yahan sirf bacha hua data check hota hai.
SELECT
    'total_amount_pkr' AS measure,
    MIN(total_amount_pkr) AS min_value,
    MAX(total_amount_pkr) AS max_value,
    ROUND(AVG(total_amount_pkr), 2) AS avg_value,
    ROUND(STDDEV(total_amount_pkr), 2) AS std_dev,
    (SELECT COUNT(*) FROM customer_orders
      WHERE total_amount_pkr > (SELECT AVG(total_amount_pkr) + 2 * STDDEV(total_amount_pkr)
                                FROM customer_orders)) AS records_above_2_std_dev
FROM customer_orders
UNION ALL
SELECT
    'unit_price_pkr',
    MIN(unit_price_pkr),
    MAX(unit_price_pkr),
    ROUND(AVG(unit_price_pkr), 2),
    ROUND(STDDEV(unit_price_pkr), 2),
    (SELECT COUNT(*) FROM customer_orders
      WHERE unit_price_pkr > (SELECT AVG(unit_price_pkr) + 2 * STDDEV(unit_price_pkr)
                              FROM customer_orders))
FROM customer_orders
UNION ALL
SELECT
    'quantity',
    MIN(quantity),
    MAX(quantity),
    ROUND(AVG(quantity), 2),
    ROUND(STDDEV(quantity), 2),
    (SELECT COUNT(*) FROM customer_orders
      WHERE quantity > (SELECT AVG(quantity) + 2 * STDDEV(quantity)
                        FROM customer_orders))
FROM customer_orders;