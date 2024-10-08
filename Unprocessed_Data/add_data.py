import os
from pathlib import Path
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

from csst.experiment import Experiment
from csst.db.adder import add_processed_reactor, add_experiment
from csst.analyzer import Analyzer

logging.basicConfig(filename='csst_db_experiment_add_errors.log', encoding='utf-8', level=logging.WARNING)

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
Session = sessionmaker(engine)


query = """SELECT file_name FROM csst_experiments"""
with engine.connect() as conn, conn.begin():
    df = pd.read_sql_query(text(query), conn)

already_added = set(df.file_name.to_list())

folder = Path("data")

files = list(folder.glob('**/*.csv'))

for i, file in enumerate(files):
    print(f"{i} / {len(files)}")
    if file.name in already_added:
        continue
    try:
        print(f"Adding: {file}")
        exp = Experiment.load_from_file(file)
    except Exception as e:
        logging.error(f"Issue adding file {file}")
        logging.error(e)
        print(e)
        continue
    with Session() as session:
        try:
            analyzer = Analyzer()
            analyzer.add_experiment_reactors(exp)
            add_experiment(exp, session)
            for reactor in analyzer.processed_reactors:
                add_processed_reactor(session=session, reactor=reactor)
        except Exception as e:
            logging.error(f"Issue adding file {file}")
            print(e)
            session.rollback()
        else:
            session.commit()
