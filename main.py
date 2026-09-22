import pandas as pd
from db_extraction.extract_db_data import fetch_db_data
from adapters.ConfigAdapter import ConfigAdapter
from YamlHandler import YamlHandler


if __name__ == '__main__':

    excel_path = 'pricing_files/cennik_siot.xlsx'

    config = ConfigAdapter(YamlHandler.data)

    db_df = fetch_db_data()

    excel_df = config.extract(excel_path)
    excel_df = config.transform(excel_df)

    result_df = db_df.merge(
        excel_df,
        left_on='Kod_Dostawcy',
        right_on='code_pricelist',
        how='left'
    )

    result_df['price_diff'] = ((result_df['price_pricelist'] - result_df[YamlHandler.currency_key[1]])
                               /result_df[YamlHandler.currency_key[1]].replace(0, pd.NA))
 
    result_df.to_excel('test.xlsx')

