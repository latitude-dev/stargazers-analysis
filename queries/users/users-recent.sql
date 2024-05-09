-- Return the users created after the repo creation date
SELECT count(*) as total
FROM { ref('users/users-base') } u
WHERE u.created_at::date >= '2024-03-15'