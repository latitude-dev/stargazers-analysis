SELECT 
    location
FROM { ref('users/users-base') }
GROUP BY 1
