{@const organization_search = param("organization_search", "")}
{@const organization_total = param("organization_total", "")}

SELECT organization, count(organization) as total
FROM read_csv_auto('queries/organizations.csv', HEADER=TRUE)
WHERE 1 = 1
{#if organization_search != 'All Organizations'}
  AND organization = {organization_search}
{/if}
GROUP BY 1
{#if organization_total}
HAVING total >= {organization_total}
{/if}
ORDER BY 2 DESC
