{@const repo_search = param("repo_search", "")}
{@const repo_total = param("repo_total", "")}

SELECT starred_repo, count(starred_repo) as total
FROM read_csv_auto('queries/repos.csv', HEADER=TRUE)
WHERE 1=1
{#if repo_search != 'All Repos'}
  AND starred_repo = {repo_search}
{/if}
GROUP BY 1
{#if repo_total}
HAVING total >= {repo_total}
{/if}
ORDER BY 2 DESC

LIMIT 500