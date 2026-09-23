import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def fetch_db_data(supplier_code: str, config) -> pd.DataFrame:

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
                TW.Twr_Kod AS [Kod],
                TRIM(TW.Twr_KodDostawcy) AS [Kod_Dostawcy],
                MAX(CASE WHEN TC.TwC_TwCNumer = 2 THEN TC.TwC_Wartosc END) AS [Cena_Cennikowa],
                MAX(CASE WHEN TC.TwC_TwCNumer = {config.currency_id} THEN TC.TwC_Wartosc END) AS [{config.currency_name}]
                FROM CDN.Towary TW
                LEFT JOIN CDN.TwrCeny TC ON TW.Twr_TwrId = TC.TwC_TwrID
                LEFT JOIN CDN.Kontrahenci K ON TW.Twr_KntId = K.Knt_KntId
                WHERE K.Knt_Kod = '{config.supplier_code}' AND TW.Twr_KodDostawcy <> ''
                GROUP BY TW.Twr_Kod, TW.Twr_KodDostawcy, K.Knt_Kod
            """
            db_df = pd.read_sql(query, connection)
        return db_df
    except Exception as e:
        print(e)
        return pd.DataFrame()

