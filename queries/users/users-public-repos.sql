-- Return the users created after the repo creation date
SELECT count(*) as total
FROM { ref('users/users-base') } u
WHERE u.public_repos_count >= 5