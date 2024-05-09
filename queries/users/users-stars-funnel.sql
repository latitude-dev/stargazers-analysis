SELECT 'All Users' AS range, COUNT(*) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>1 Repos' AS range, COUNT(CASE WHEN starred_repos_count >= 1 THEN 1 END) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>500 Repos' AS range, COUNT(CASE WHEN starred_repos_count >= 500 THEN 1 END) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>1000 Repos' AS range, COUNT(CASE WHEN starred_repos_count >= 1000 THEN 1 END) AS users
FROM { ref('users/users-base') }
UNION ALL
SELECT '>5000 Repos' AS range, COUNT(CASE WHEN starred_repos_count >= 5000 THEN 1 END) AS users
FROM { ref('users/users-base') }
