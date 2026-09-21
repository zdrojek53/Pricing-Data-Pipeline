import pandas as pd
from db_extraction.extract_db_data import fetch_db_data


def clean_excel(excel_data):
    excel_data = (
            excel_data.dropna(subset=["Code"])
            .fillna({"Net price": 0})
            .drop_duplicates(subset=["Code"])
            )
    excel_data["Code"] = excel_data["Code"].astype('str').str.strip()
    excel_data["Net price"] = excel_data["Net price"].astype('float64')

    return excel_data


if __name__ == '__main__':
    db_df = fetch_db_data()
    excel_df = pd.read_excel('pricing_files/cennik_siot.xlsx', usecols=["Code", "Net price"])
    excel_df = clean_excel(excel_df)
    result_df = db_df.merge(
        excel_df,
        left_on="Kod_Dostawcy",
        right_on="Code",
        how="left"
    )
 
    result_df.to_excel('test.xlsx')
