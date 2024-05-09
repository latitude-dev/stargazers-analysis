SELECT 
    username
FROM {ref ('filters/organizations-params')}
GROUP BY username