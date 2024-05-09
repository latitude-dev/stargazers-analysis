-- Return the total number of users
SELECT count(*) as total
FROM { ref('users/users-base') } u