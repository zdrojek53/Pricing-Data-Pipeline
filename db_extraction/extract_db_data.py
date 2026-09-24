import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


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

    try:
        with engine.connect() as connection:
            query = f"""
                SELECT
                TW.{os.getenv('DB_PRODUCT_CODE')} AS [Kod],
                TRIM(TW.{os.getenv('DB_SUPPLIER_CODE')}) AS [Kod_Dostawcy],
                MAX(CASE WHEN TC.{os.getenv('DB_PRICE_ID')} = 2 THEN TC.{os.getenv('DB_PRICE')} END) AS [Cena_Cennikowa],
                MAX(CASE WHEN TC.{os.getenv('DB_PRICE_ID')} = {config.currency_id} THEN TC.{os.getenv('DB_PRICE')} END) AS [{config.currency_name}],
                MAX(CASE WHEN TA.{os.getenv('DB_ATTR_ID')} = {os.getenv('DB_ATTR')} THEN TA.{os.getenv('DB_ATTR_TXT')} END) AS [Marza]
                FROM {os.getenv('DB_PRODUCTS')} TW
                LEFT JOIN {os.getenv('DB_PRICES')} TC ON TW.{os.getenv('DB_PRODUCT_ID')} = TC.{os.getenv('DB_PRICES_PRODUCT_ID')}
                LEFT JOIN {os.getenv('DB_CLIENTS')} K ON TW.{os.getenv('DB_PRODUCTS_CLIENT_ID')} = K.{os.getenv('DB_CLIENT_ID')}
                LEFT JOIN {os.getenv('DB_ATTRIBUTES')} TA ON TW.{os.getenv('DB_PRODUCT_ID')} = TA.{os.getenv('DB_ATTR_PRODUCT_ID')}
                WHERE K.{os.getenv('DB_CLIENT_CODE')} = '{config.supplier_code}' AND TW.{os.getenv('DB_SUPPLIER_CODE')} <> ''
                GROUP BY TW.{os.getenv('DB_PRODUCT_CODE')}, TW.{os.getenv('DB_SUPPLIER_CODE')}, K.{os.getenv('DB_CLIENT_CODE')}
            """
            db_df = pd.read_sql(query, connection)
        return db_df
    except Exception as e:
        print(e)
        return pd.DataFrame()

