{@const users_organization_search = param("users_organization_search", "")}
SELECT 
    username
    ,organization
FROM read_csv_auto('queries/organizations.csv', HEADER=TRUE)
WHERE 1=1
{#if users_organization_search != 'All Organizations'}
  AND organization LIKE '%' || {users_organization_search} || '%'
{/if}