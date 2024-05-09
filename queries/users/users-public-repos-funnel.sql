SELECT 'All users' AS range, COUNT(*) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>1 Repos' AS range, COUNT(CASE WHEN public_repos_count >= 1 THEN 1 END) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>5 Repos' AS range, COUNT(CASE WHEN public_repos_count >= 5 THEN 1 END) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>10 Repos' AS range, COUNT(CASE WHEN public_repos_count >= 10 THEN 1 END) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>50 Repos' AS range, COUNT(CASE WHEN public_repos_count >= 50 THEN 1 END) AS users
FROM { ref('users/users-base') }
