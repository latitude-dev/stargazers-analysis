SELECT following as user, count(following) as total
FROM read_csv_auto('queries/following.csv', HEADER=TRUE)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 25