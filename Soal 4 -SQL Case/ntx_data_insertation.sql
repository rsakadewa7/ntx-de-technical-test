BULK INSERT EcommerceData
FROM 'C:\Users\rsaka\Downloads\TEST\ntx\ntx-de-technical-test\Soal 1 - Data Transformation dan Analysis Case\ecommerce-session-bigquery.csv'
WITH (
    FORMAT='CSV',
    FIRSTROW=2,  -- Skip header row
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    TABLOCK
);
