SELECT 
    username
FROM {{ref ('filters/users-params')}
GROUP BY 1