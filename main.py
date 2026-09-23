from db_extraction.extract_db_data import fetch_db_data
from adapters.ConfigAdapter import ConfigAdapter
from YamlHandler import YamlHandler
from pathlib import Path
from dotenv import load_dotenv


def run_pipeline(config_path: str | Path, excel_path: str):

    load_dotenv()
    
    config = YamlHandler(config_path)
    handled_config = ConfigAdapter(config.data)
    
    db_df = fetch_db_data("siot", config)
    
    excel_df = handled_config.extract(excel_path)
    excel_df = handled_config.transform(excel_df)
    
    result_df = db_df.merge(
        excel_df,
        left_on='Kod_Dostawcy',
        right_on='code_pricelist',
        how='left'
    )
    
    result_df['price_diff'] = ((result_df['price_pricelist'] - result_df[config.currency_key[1]])
                                /result_df[config.currency_key[1]].replace(0, float('nan')))
     
    result_df.to_excel('test.xlsx', index=False)


if __name__ == '__main__':
    run_pipeline(Path(__file__).resolve().parent / 'configs' / 'siot.yaml', 'pricing_files/cennik_siot.xlsx')
    

