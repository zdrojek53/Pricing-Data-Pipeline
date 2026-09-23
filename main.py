from db_extraction.extract_db_data import fetch_db_data
from adapters.ConfigAdapter import ConfigAdapter
from YamlHandler import YamlHandler
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

def run_pipeline(config: YamlHandler, excel_path: str):

    
    handled_config = ConfigAdapter(config.data)
    
    db_df = fetch_db_data("siot", config)

    if db_df.empty:
        raise ConnectionError('Błąd połączenia z bazą danych.')
    
    excel_df = handled_config.extract(excel_path)
    excel_df = handled_config.transform(excel_df)
    
    result_df = db_df.merge(
        excel_df,
        left_on='Kod_Dostawcy',
        right_on='code_pricelist',
        how='left'
    )
    
    result_df['price_diff'] = ((result_df['price_pricelist'] - result_df[config.currency_name])
                                /result_df[config.currency_name].replace(0, float('nan')))
     
    result_df.to_excel('test.xlsx', index=False)


if __name__ == '__main__':
    for cfg in Path('configs').glob('*.yaml'):
        config = YamlHandler(cfg)
        run_pipeline(config, config.file_path)
    

