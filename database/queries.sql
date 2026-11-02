-- queries.sql

SET search_path TO search_engine;

-- 1. JOIN: every document with its source name
SELECT d.title, s.name AS source
FROM documents d
JOIN sources s ON s.source_id = d.source_id;

-- 2. LEFT JOIN + NULL: sources that have NO documents
SELECT s.name
FROM sources s
LEFT JOIN documents d ON d.source_id = s.source_id
WHERE d.document_id IS NULL;

-- 3. GROUP BY + HAVING: sources with more than 2 documents
SELECT s.name, COUNT(*) AS doc_count
FROM sources s
JOIN documents d ON d.source_id = s.source_id
GROUP BY s.name
HAVING COUNT(*) > 2
ORDER BY doc_count DESC;

-- 4. COALESCE + CASE: label uncategorized docs, bucket by recency
SELECT
    title,
    COALESCE(c.name, 'Uncategorized') AS category,
    CASE
        WHEN published_date >= DATE '2026-09-15' THEN 'recent'
        WHEN published_date >= DATE '2026-09-05' THEN 'mid'
        ELSE 'older'
    END AS age_bucket
FROM documents d
LEFT JOIN categories c ON c.category_id = d.category_id;

-- 5. Subquery: documents from the busiest source
SELECT title
FROM documents
WHERE source_id = (
    SELECT source_id FROM documents
    GROUP BY source_id ORDER BY COUNT(*) DESC LIMIT 1
);

-- 6. EXISTS: documents that have an author in their metadata
SELECT d.title
FROM documents d
WHERE EXISTS (
    SELECT 1 FROM document_metadata m
    WHERE m.document_id = d.document_id AND m.key = 'author'
);

-- 7. CTE: docs per category, then only categories above average
WITH per_category AS (
    SELECT c.name, COUNT(*) AS n
    FROM categories c
    JOIN documents d ON d.category_id = c.category_id
    GROUP BY c.name
)
SELECT name, n
FROM per_category
WHERE n > (SELECT AVG(n) FROM per_category);

-- 8. UNION: all distinct "labels" in the system (sources + categories)
SELECT name, 'source' AS kind FROM sources
UNION
SELECT name, 'category' FROM categories;

-- 9. Window: each document next to how many docs its source has
--    (shows every row, unlike GROUP BY which collapses rows)
SELECT
    title,
    source_id,
    COUNT(*) OVER (PARTITION BY source_id) AS docs_in_source
FROM documents;

-- 10. ROW_NUMBER: the newest document per source
SELECT *
FROM (
    SELECT
        s.name AS source,
        d.title,
        d.published_date,
        ROW_NUMBER() OVER (
            PARTITION BY d.source_id
            ORDER BY d.published_date DESC
        ) AS rn
    FROM documents d
    JOIN sources s ON s.source_id = d.source_id
) ranked
WHERE rn = 1;

-- 11. RANK: rank categories by how many documents they hold
SELECT
    c.name,
    COUNT(*) AS n,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS popularity_rank
FROM categories c
JOIN documents d ON d.category_id = c.category_id
GROUP BY c.name;

-- 12. LAG / LEAD: days between consecutive documents from one source
SELECT
    title,
    published_date,
    published_date - LAG(published_date) OVER (
        PARTITION BY source_id ORDER BY published_date
    ) AS days_since_previous,
    LEAD(title) OVER (
        PARTITION BY source_id ORDER BY published_date
    ) AS next_title
FROM documents
WHERE source_id = 1;

-- 13. The view, plus the first taste of search (Week 7 preview)
SELECT document_id, title, source_name, category
FROM v_document_details
WHERE title ILIKE '%waterloo%';

-- 14. Transaction: all-or-nothing insert (ROLLBACK undoes it)
BEGIN;
    INSERT INTO sources (name, type) VALUES ('Temp Source', 'api');
    INSERT INTO documents (source_id, title, content_hash)
    VALUES (currval(pg_get_serial_sequence('sources','source_id')), 'Temp doc', 'tmp1');
ROLLBACK;  -- change to COMMIT to keep it

-- 15. Ask the planner for its plan. On 10 rows it will pick a Seq Scan
--     (cheaper than an index on tiny tables); bulk-load data in Week 4+ and re-run.
EXPLAIN SELECT * FROM documents WHERE published_date >= '2026-09-15';