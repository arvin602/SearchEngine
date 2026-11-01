-- schema.sql  |  Data Search Engine, 
-- Run order: schema.sql -> seed.sql -> queries.sql
-- ------------------------------------------------------------

DROP SCHEMA IF EXISTS search_engine CASCADE;
CREATE SCHEMA search_engine;
SET search_path TO search_engine;


-- sources
-- ------------------------------------------------------------
CREATE TABLE sources (
    source_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT        NOT NULL UNIQUE,
    url         TEXT,
    type        TEXT        NOT NULL
                CHECK (type IN ('api', 'csv', 'website', 'database')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- categories
-- ------------------------------------------------------------

CREATE TABLE categories (
    category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE
);


-- documents
-- ------------------------------------------------------------
CREATE TABLE documents (
    document_id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id      INTEGER     NOT NULL
                   REFERENCES sources(source_id) ON DELETE RESTRICT,
    category_id    INTEGER
                   REFERENCES categories(category_id) ON DELETE SET NULL,
    title          TEXT        NOT NULL CHECK (length(trim(title)) > 0),
    content        TEXT,
    published_date DATE,
    content_hash   TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, content_hash)
);


-- document_metadata (key/value facts about a document)
-- ------------------------------------------------------------
CREATE TABLE document_metadata (
    metadata_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id INTEGER NOT NULL
                REFERENCES documents(document_id) ON DELETE CASCADE,
    key         TEXT NOT NULL,
    value       TEXT,
    UNIQUE (document_id, key)
);


-- Indexes
-- ------------------------------------------------------------
CREATE INDEX idx_documents_source_id  ON documents(source_id);
CREATE INDEX idx_documents_category_id ON documents(category_id);
CREATE INDEX idx_documents_published  ON documents(published_date);
CREATE INDEX idx_metadata_document_id ON document_metadata(document_id);

-- View (query for future API)
-- ------------------------------------------------------------
CREATE VIEW v_document_details AS
SELECT
    d.document_id,
    d.title,
    d.content,
    d.published_date,
    s.name  AS source_name,
    s.type  AS source_type,
    COALESCE(c.name, 'Uncategorized') AS category
FROM documents d
JOIN sources s            ON s.source_id = d.source_id
LEFT JOIN categories c    ON c.category_id = d.category_id;