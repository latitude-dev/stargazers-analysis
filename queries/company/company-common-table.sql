{@const company_search = param("company_search", "")}
{@const company_total = param("company_total", "")}

SELECT company as company, count(company) as total
FROM read_csv_auto('queries/user-details.csv', HEADER=TRUE)
WHERE 1=1
{#if company_search != 'All Companies'}
  AND company = {company_search}
{/if}
GROUP BY 1
{#if company_total}
HAVING total >= {company_total}
{/if}
ORDER BY 2 DESC