{@const users_following_search = param("users_following_search", "")}
SELECT 
    username
    ,following
FROM read_csv_auto('queries/following.csv', HEADER=TRUE)
WHERE 1=1
{#if users_following_search != 'All Following'}
  AND following LIKE '%' || {users_following_search} || '%'
{/if}