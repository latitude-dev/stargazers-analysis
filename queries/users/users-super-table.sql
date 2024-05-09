
SELECT 
    u.username as usernameu
    ,email
    ,TRIM(SPLIT_PART(location, ',', 1)) AS location
    ,created_at
    ,updated_at
    ,followers_count
    ,following_count
    ,public_repos_count
    ,starred_repos_count
    ,starred_repo
FROM read_csv_auto('queries/user-details.csv', HEADER=TRUE) u
