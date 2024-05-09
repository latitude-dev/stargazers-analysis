SELECT 
    username
FROM {ref ('filters/following-params')}
GROUP BY username