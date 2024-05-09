SELECT 
    starred_repo, count(*) as total
FROM read_csv_auto('queries/repos.csv', HEADER=TRUE)
GROUP BY 1
HAVING 
    total >= 80
ORDER BY total DESC
