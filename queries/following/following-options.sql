SELECT 
    following, count(*) as total
FROM read_csv_auto('queries/following.csv', HEADER=TRUE)
GROUP BY 1
ORDER BY total DESC
LIMIT 500