import os
import logging
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pathlib import Path

load_dotenv()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
SQL_PATH = BASE_DIR / 'queries' / 'fetch_products.sql'

def fetch_db_data(config) -> pd.DataFrame:

    connection_url = URL.create(
        'mssql+pyodbc',
        host=os.getenv('DB_SERVER'),
        database=os.getenv('DB_NAME'),
        query={
            'driver': os.getenv('DB_DRIVER', 'ODBC Driver 18 for SQL Server'),
            'trusted_connection': 'yes',
            'Encrypt': 'yes',
            'TrustServerCertificate': 'yes'
        }
    )

    engine = create_engine(connection_url)

    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        query_str = f.read()

    params = {
        'supplier_code': config.supplier_code,
        'currency_id': config.currency_id,
        'margin_attr_id': os.getenv('DB_MARGIN_ATTR', 1),
        'factor_attr_id': os.getenv('DB_FACTOR_ATTR', 1)
    }

    try:
        with engine.connect() as connection:
            db_df = pd.read_sql(text(query_str), connection, params=params)

        if 'Cena_Waluta' in db_df.columns:
            db_df.rename(columns={'Cena_Waluta': config.currency_name}, inplace=True)

        return db_df

    except Exception as e:
        logger.exception("Failed to connect to db")
        return pd.DataFrame()

