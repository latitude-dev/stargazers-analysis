SELECT 
    username
FROM {ref ('filters/repos-params')}
GROUP BY username