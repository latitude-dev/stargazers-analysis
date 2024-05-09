SELECT 
    username
    ,email
    ,TRIM(SPLIT_PART(location, ',', 1)) AS location
    ,company
    ,created_at
    ,updated_at
    ,followers_count
    ,following_count
    ,public_repos_count
    ,starred_repos_count
FROM read_csv_auto('queries/user-details.csv', HEADER=TRUE)