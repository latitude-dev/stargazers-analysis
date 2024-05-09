-- This query retrieve the list of users taking into account all the filters

{@const users_repo_search = param("users_repo_search", "")}
{@const users_following_search = param("users_following_search", "")}
{@const users_organization_search = param("users_organization_search", "")}
{@const users_followers_count = param("users_followers_count", 0)}
{@const users_following_count = param("users_following_count", 0)}
{@const users_public_repos_count = param("users_public_repos_count", 0)}
{@const users_starred_repos_count = param("users_starred_repos_count", 0)}


SELECT 
    username
    ,case when email is null then '-' else email end as email
    ,case when location is null then '-' else TRIM(SPLIT_PART(location, ',', 1)) end as location
    ,FORMAT(created_at, '%Y-%m-%d') created_at
    ,FORMAT(updated_at, '%Y-%m-%d') updated_at
    ,followers_count as followers
    ,following_count as following
    ,public_repos_count as public_repos
    ,starred_repos_count as starred_repos
FROM read_csv_auto('queries/user-details.csv', HEADER=TRUE, DATEFORMAT = '%m/%d/%Y')
WHERE 1=1

{#if param('users_user_search', false)}
  AND (lower(username) LIKE '%' || lower({param('users_user_search')}) || '%'
  OR lower(email) LIKE '%' || lower({param('users_user_search')}) || '%'
  OR lower(location) LIKE '%' || lower({param('users_user_search')}) || '%')
{/if}
{#if users_repo_search != 'All Repos'}
  AND username IN ({ref ('filters/get-repos-filtered')})
{/if}
{#if users_organization_search != 'All Organizations'}
  AND username IN ({ref ('filters/get-organizations-filtered')})
{/if}
{#if users_following_search != 'All Following'}
  AND username IN ({ref ('filters/get-following-filtered')})
{/if}
{#if param('users_followers_count', 0)}
  AND followers_count >= {users_followers_count}
{/if}
{#if param('users_following_count', 0)}
  AND following_count >= {users_following_count}
{/if}
{#if param('users_public_repos_count', 0)}
  AND public_repos_count >= {users_public_repos_count}
{/if}
{#if param('users_starred_repos_count', 0)}
  AND starred_repos_count >= {users_starred_repos_count}
{/if}
ORDER BY user DESC