import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

from csst.db import Base

dotenv_path = Path(__file__).parent.absolute() / ".env"
if not dotenv_path.exists():
    raise FileNotFoundError(
        ".env file must be created in this folder with CSST_DB_USER, "
        + "CSST_DB_PASSWORD, CSST_DB_HOST, CSST_DB_PORT, and CSST_DB_NAME"
    )
load_dotenv(str(dotenv_path))

db_server = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
    os.environ.get("CSST_DB_USER"),
    os.environ.get("CSST_DB_PASSWORD"),
    os.environ.get("CSST_DB_HOST"),
    int(os.environ.get("CSST_DB_PORT")),
    os.environ.get("CSST_DB_NAME"),
)

engine = create_engine(db_server)
if not database_exists(engine.url):
    print("Creating database")
    create_database(engine.url)
    Base.metadata.create_all(engine)

table_folder = Path('database_tables')
tables = [
    "polymers",
    "solvents",
    "lab_polymers",
    "lab_solvents"
]
for table in tables:
    print(f"Adding {table}")
    df = pd.read_csv(str(table_folder / f"{table}.csv")) 
    df.to_sql(table, engine, if_exists='append', index=False)

print("Database creation complete")
