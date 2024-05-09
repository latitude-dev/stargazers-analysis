{@const users_repo_search = param("users_repo_search", "")}
SELECT 
    username
    ,starred_repo
FROM read_csv_auto('queries/repos.csv', HEADER=TRUE)
WHERE 1=1
{#if users_repo_search != 'All Repos'}
  AND starred_repo LIKE '%' || {users_repo_search} || '%'
{/if}