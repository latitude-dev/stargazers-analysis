SELECT 
    company
FROM { ref('users/users-base') }
GROUP BY 1
