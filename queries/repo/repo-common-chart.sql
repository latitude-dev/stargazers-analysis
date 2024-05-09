SELECT TRIM(SPLIT_PART(starred_repo, '/', 2)) AS starred_repo, TRIM(SPLIT_PART(starred_repo, '/', 1)) AS organization, count(starred_repo) as total
FROM read_csv_auto('queries/repos.csv', HEADER=TRUE)
GROUP BY starred_repo, organization
ORDER BY total DESC
LIMIT 25