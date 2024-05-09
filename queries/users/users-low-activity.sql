-- Return the users created after the repo creation date
SELECT count(*) as total
FROM { ref('users/users-base') } u
WHERE u.following_count < 5 
AND u.followers_count < 5
AND u.public_repos_count < 2