-- seed.sql: fake dataset to use and test queries on

SET search_path TO search_engine;

INSERT INTO sources (name, url, type) VALUES
  ('Waterloo News API',   'https://example.com/api/news', 'api'),
  ('City Open Data CSV',  'https://example.com/data.csv', 'csv'),
  ('Tech Blog Scraper',   'https://example.com/blog',     'website'),
  ('Unused Source',       NULL,                           'database');

INSERT INTO categories (name) VALUES
  ('Technology'), ('Transportation'), ('Education'), ('Health');

INSERT INTO documents (source_id, category_id, title, content, published_date, content_hash) VALUES
  (1, 1, 'Waterloo startup raises seed round', 'A Waterloo software startup announced funding...', '2026-09-01', 'h01'),
  (1, 3, 'University of Waterloo opens new lab', 'The engineering faculty opened a robotics lab...', '2026-09-03', 'h02'),
  (1, 2, 'LRT service changes announced',       'Grand River Transit updates ION schedules...',     '2026-09-10', 'h03'),
  (1, 1, 'Local AI meetup draws record crowd',  'Over 300 attendees gathered in Kitchener...',      '2026-09-15', 'h04'),
  (2, 2, 'Road closures this fall',             'Construction on King St continues...',             '2026-09-05', 'h05'),
  (2, 2, 'Bike lane usage report',              'Cycling trips rose 12 percent...',                 '2026-09-20', 'h06'),
  (2, 4, 'Public health clinic hours',          'Clinics extend evening hours...',                  '2026-09-22', 'h07'),
  (3, 1, 'Intro to PostgreSQL indexes',         'Indexes speed up lookups by...',                   '2026-08-28', 'h08'),
  (3, 1, 'Why window functions matter',         'Window functions let you compute...',              '2026-09-12', 'h09'),
  (3, NULL, 'Untagged post about Waterloo',     'A post with no category yet...',                   '2026-09-25', 'h10');

INSERT INTO document_metadata (document_id, key, value) VALUES
  (1, 'author', 'A. Singh'),   (1, 'language', 'en'),
  (2, 'author', 'M. Chen'),    (2, 'language', 'en'),
  (3, 'language', 'en'),
  (8, 'author', 'J. Patel'),   (8, 'language', 'en'),
  (9, 'author', 'J. Patel'),   (9, 'language', 'en');