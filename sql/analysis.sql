-- PostgreSQL: Enterprise data quality monitoring
-- Import data/dataset.csv as enterprise_quality_records

-- 1. Overall quality status
SELECT quality_status, COUNT(*) AS records,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM enterprise_quality_records
GROUP BY quality_status ORDER BY records DESC;

-- 2. Failure rates by source system
SELECT source_system,
       COUNT(*) AS records,
       ROUND(100.0 * AVG(1-email_present),2) AS missing_email_pct,
       ROUND(100.0 * AVG(1-postcode_valid),2) AS invalid_postcode_pct,
       ROUND(100.0 * AVG(duplicate_flag),2) AS duplicate_pct,
       ROUND(100.0 * AVG(1-pii_format_valid),2) AS pii_format_failure_pct
FROM enterprise_quality_records
GROUP BY source_system ORDER BY records DESC;

-- 3. Daily exception trend
SELECT ingestion_date, COUNT(*) FILTER (WHERE quality_status <> 'PASS') AS exception_records
FROM enterprise_quality_records GROUP BY ingestion_date ORDER BY ingestion_date;
