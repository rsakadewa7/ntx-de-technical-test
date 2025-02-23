-- 1
WITH TopCountries AS (
    SELECT TOP 5 
        country, 
        SUM(totalTransactionRevenue) AS total_revenue
    FROM EcommerceData
    WHERE totalTransactionRevenue IS NOT NULL
    GROUP BY country
    ORDER BY SUM(totalTransactionRevenue) DESC
)
SELECT 
    e.country,
    e.channelGrouping,
    SUM(e.totalTransactionRevenue) AS total_channel_revenue
FROM EcommerceData e
INNER JOIN TopCountries tc 
    ON e.country = tc.country
WHERE e.totalTransactionRevenue IS NOT NULL
GROUP BY e.country, e.channelGrouping
ORDER BY e.country, SUM(e.totalTransactionRevenue) DESC;


-- 2
WITH UserMetrics AS (
    SELECT 
        fullVisitorId,
        AVG(timeOnSite) AS avg_time_on_site,
        AVG(pageviews) AS avg_pageviews,
        AVG(sessionQualityDim) AS avg_session_quality
    FROM EcommerceData
    WHERE timeOnSite IS NOT NULL AND pageviews IS NOT NULL
    GROUP BY fullVisitorId
),
OverallAverages AS (
    SELECT 
        AVG(avg_time_on_site) AS overall_avg_time,
        AVG(avg_pageviews) AS overall_avg_pageviews
    FROM UserMetrics
)
SELECT 
    u.fullVisitorId,
    u.avg_time_on_site,
    u.avg_pageviews,
    u.avg_session_quality
FROM UserMetrics u
CROSS JOIN OverallAverages o
WHERE u.avg_time_on_site > o.overall_avg_time
AND u.avg_pageviews < o.overall_avg_pageviews
ORDER BY u.avg_time_on_site DESC;

-- Since the sessionQualityDim has (19 non-null values out of 10,000 rows)
-- most users will have NULL for avg_session_quality

-- 3
WITH ProductMetrics AS (
    SELECT 
        v2ProductName AS product_name,
        SUM(productRevenue) AS total_revenue,
        SUM(productQuantity) AS total_quantity_sold,
        SUM(productRefundAmount) AS total_refund_amount,
        (SUM(productRevenue) - SUM(productRefundAmount)) AS net_revenue
    FROM EcommerceData
    GROUP BY v2ProductName
),
RankedProducts AS (
    SELECT 
        product_name,
        total_revenue,
        total_quantity_sold,
        total_refund_amount,
        net_revenue,
        RANK() OVER (ORDER BY net_revenue DESC) AS revenue_rank,
        CASE 
            WHEN total_refund_amount > (0.1 * total_revenue) THEN 'Flagged'
            ELSE 'OK'
        END AS refund_flag
    FROM ProductMetrics
)
SELECT * FROM RankedProducts
ORDER BY revenue_rank;

-- A. Missing Values in Key Metrics
-- total_revenue, total_quantity_sold, and total_refund_amount are mostly NULL.
-- This could be due to incomplete data extraction or incorrect joins.
-- Solution: Check raw data sources and ensure correct table joins. Use COALESCE() to replace NULL with 0.

-- B. Incorrect Revenue Ranking
-- Since net_revenue is NULL, all products have the same rank (1).
-- Solution: Ensure net_revenue = total_revenue - total_refund_amount is calculated correctly before ranking.

-- C. Refund Flagging is Not Working
-- Refund flag is always "OK" because total_refund_amount is NULL.
-- Solution: Verify refund data is included and ensure correct aggregation.

-- 4 


