SELECT avg(followers_count) as total
FROM read_csv_auto('queries/following.csv', HEADER=TRUE)