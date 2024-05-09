{@const location_search = param("location_search", "")}
{@const location_total = param("location_total", "")}

SELECT TRIM(SPLIT_PART(location, ',', 1)) AS location, count(location) as total
FROM read_csv_auto('queries/user-details.csv', HEADER=TRUE)
WHERE 1=1
{#if location_search != 'All Locations'}
  AND location = {location_search}
{/if}
GROUP BY 1
{#if location_total}
HAVING total >= {location_total}
{/if}
ORDER BY 2 DESC