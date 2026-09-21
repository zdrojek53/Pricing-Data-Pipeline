import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def fetch_db_data():
    load_dotenv()

    connection_url = URL.create(
        "mssql+pyodbc",
        host=os.getenv("DB_SERVER"),
        database=os.getenv("DB_NAME"),
        query={
            "driver": os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server"),
            "trusted_connection": "yes",
            "Encrypt": "yes",
            "TrustServerCertificate": "yes"
        }
    )

    engine = create_engine(connection_url)

    try:
        with engine.connect() as connection:
            db_df = pd.read_sql(
                text("""SELECT
                TW.Twr_Kod AS [Kod],
                TRIM(TW.Twr_KodDostawcy) AS [Kod_Dostawcy],
                MAX(CASE WHEN TC.TwC_TwCNumer = 2 THEN TC.TwC_Wartosc END) AS [Cena_Cennikowa],
                MAX(CASE WHEN TC.TwC_TwCNumer = 7 THEN TC.TwC_Wartosc END) AS [Cena_CZK]
                FROM CDN.Towary TW
                LEFT JOIN CDN.TwrCeny TC ON TW.Twr_TwrId = TC.TwC_TwrID
                LEFT JOIN CDN.Kontrahenci K ON TW.Twr_KntId = K.Knt_KntId
                WHERE K.Knt_Kod = 'SIOT' AND TW.Twr_KodDostawcy <> ''
                GROUP BY TW.Twr_Kod, TW.Twr_KodDostawcy, K.Knt_Kod"""),
                connection
            )

        return db_df

    except Exception as e:
        print(f"Błąd połączenia z bazą: {e}")
        return None

