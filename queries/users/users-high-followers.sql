-- Return the stargazers of your repo with max number of followers
SELECT username, followers_count as total
FROM { ref('users/users-base') } u
order by followers_count desc
LIMIT 25