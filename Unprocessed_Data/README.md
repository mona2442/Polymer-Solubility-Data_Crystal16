# Unprocessed CSST data
To process the raw data, you can use our [crystal16 analyzer package](https://github.com/Ramprasad-Group/csst_analyzer). Note, we use a Postgres database to house metadata related to our experiments as well as processed data results. To use our database set up, download Postgres and a database manager (such as [dbeaver](https://dbeaver.io/)), then create a new role and password for yourself and give the role super user, can login, and create database privileges. 

We also use [poetry](https://python-poetry.org/docs/) to manage python dependencies. You can install a virtual environment in this folder that has all requisite dependencies by first downloading python 3.9, then running `poetry env use path/to/python3.9_executable/bin/python` (the actual executable path), then by running `poetry install` from the command line in this folder. 

## Database Creation
After setting up your virtual environment, modify the `.env` file in the Unprocessed_Data folder. In this file, modfiy the user and password with the role you configured.
```bash
CSST_DB_USER="your_postgres_role/username"
CSST_DB_PASSWORD="your_postgres_user_password"
CSST_DB_HOST="localhost"
CSST_DB_PORT="5432"
CSST_DB_NAME="crystal16"
```

You can then run the `build_database.py` script to build the database and add the polymer and solvent tables. After, run `add_data.py` to process the raw data files and add them to the database. Some example notebooks for analyzing the raw and processed data are available in the [`jupyter_notebooks` folder](jupyter_notebooks).
