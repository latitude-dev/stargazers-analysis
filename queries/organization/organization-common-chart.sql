SELECT organization, count(organization) as total
FROM read_csv_auto('queries/organizations.csv', HEADER=TRUE)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 25