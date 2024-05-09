SELECT 
    organization
FROM read_csv_auto('queries/organizations.csv', HEADER=TRUE)
GROUP BY 1