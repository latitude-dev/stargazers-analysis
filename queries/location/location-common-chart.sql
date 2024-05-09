SELECT TRIM(SPLIT_PART(location, ',', 1)) AS location, count(location) as total
FROM read_csv_auto('queries/user-details.csv', HEADER=TRUE)
WHERE 1=1
GROUP BY 1
ORDER BY 2 DESC
LIMIT 25