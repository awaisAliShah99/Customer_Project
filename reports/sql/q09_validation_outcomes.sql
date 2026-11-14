-- Q9: How many records were accepted, corrected, or rejected during data cleaning?
-- (duplicate_removed = transformation mein hate duplicate records)
SELECT
    outcome,
    records,
    ROUND(100 * records / (SELECT SUM(records) FROM validation_summary), 2) AS pct_of_raw_records
FROM validation_summary
ORDER BY records DESC;