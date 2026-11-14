Search Engine / Datapipeline 

Progress:
- PostgreSQL schema, seed data (subject to change), and some queries
- Can run live on PostgreSQL
- Python / Panda used to take CSV's and convert into readable format --> into PostgreSQL
- Pulls live data from the Hacker News API as well as CSVs (Not fully available yet)
- Cleans and validates records (missing titles, bad dates, duplicates) before loading
- Pipeline can be re-run safely

Setup:
python3 -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt. 

Create a .env file and add your database password - DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/searchdb

Database:
createdb searchdb
psql -d searchdb -f database/schema.sql
psql -d searchdb -f database/seed.sql
psql -d searchdb -f database/queries.sql
psql -d searchdb
#Run the queries

How it works:
Hacker News API --+
                  +--> clean / validate (Python) --> PostgreSQL
CSV file ---------+

fetch_data.py                    gets data from the API and CSV
etl/extract.py, transform.py     read files, clean and validate records
ingest.py                        removes duplicates, rejects bad records
db.py                            connects to PostgreSQL and loads documents
pipeline.py                      runs everything in order

Schema:
sources 1 ──< documents >── 1 categories
                 1
                 │
                 *
          document_metadata