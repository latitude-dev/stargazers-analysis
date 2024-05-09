{@const following_search = param("following_search", "")}
{@const following_total = param("following_total", "")}

SELECT following as user, count(following) as total
FROM read_csv_auto('queries/following.csv', HEADER=TRUE)
{#if following_search != 'All Users'}
  WHERE following = {following_search}
{/if}
GROUP BY 1
{#if following_total}
HAVING total >= {following_total}
{/if}
ORDER BY 2 DESC
LIMIT 500