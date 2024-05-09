SELECT company, count(company) as total
FROM read_csv_auto('queries/user-details.csv', HEADER=TRUE)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20