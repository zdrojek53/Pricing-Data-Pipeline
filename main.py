import pandas as pd
from db_extraction.extract_db_data import fetch_db_data


def clean_excel(excel_data):
    excel_data = excel_data.drop(columns=["Cat. number", "Title", "Manufacturer", "Gross price"])
    excel_data = excel_data.dropna(subset=["Code"])
    excel_data = excel_data.fillna({"Net price": 0})
    excel_data = excel_data.drop_duplicates(subset=["Code"])
    excel_data["Code"] = excel_data["Code"].astype('str').str.strip()
    excel_data["Net price"] = excel_data["Net price"].astype('float64')

    return excel_data

def clean_db(db_data):
    db_data = db_data.drop(columns=["Dostawca", "Cena_USD", "Cena_PLN", "Cena_EUR"])
    db_data["Kod_Dostawcy"] = db_data["Kod_Dostawcy"].str.strip()

    return db_data

if __name__ == '__main__':
    db_df = clean_db(fetch_db_data())
    excel_df = pd.read_excel('pricing_files/cennik_siot.xlsx')
    excel_df = clean_excel(excel_df)
    result_df = db_df.merge(
        excel_df,
        left_on="Kod_Dostawcy",
        right_on="Code",
        how="left"
    )
    print(result_df[result_df.isna().any(axis=1)].to_string())
