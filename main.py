import pandas as pd
from db_extraction.extract_db_data import fetch_db_data
from pathlib import Path
import yaml
from adapters import ConfigAdapter


if __name__ == '__main__':

    excel_path = 'pricing_files/cennik_siot.xlsx'
    yaml_path = Path(__file__).resolve().parent / 'configs' / 'siot.yaml'
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    config = ConfigAdapter.ConfigAdapter(data)

    db_df = fetch_db_data()
    excel_df = config.extract(excel_path)
    excel_df = config.transform(excel_df)
    result_df = db_df.merge(
        excel_df,
        left_on='Kod_Dostawcy',
        right_on='Code',
        how='left'
    )

    result_df['Price_diff'] = (result_df['Net price'] - result_df['Cena_CZK'])/result_df['Cena_CZK'].replace(0, pd.NA)
 
    result_df.to_excel('test.xlsx')

