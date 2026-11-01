Search Engine / Datapipeline 

Progress:
- PostgreSQL schema, seed data (subject to change), and some queries

Setup:
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

Databse:
createdb searchdb
psql -d searchdb -f database/schema.sql
psql -d searchdb -f database/seed.sql
psql -d searchdb -f database/queries.sql
