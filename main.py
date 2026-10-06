import logging
from logging_config import setup_logging
from db_extraction.extract_db_data import fetch_db_data
from adapters.excel_adapter import ExcelAdapter
from yaml_handler import YamlHandler
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)


def run_pipeline(config: YamlHandler, excel_path: str) -> None:

    handled_config = ExcelAdapter(config.config)

    db_df = fetch_db_data(config)

    if db_df.empty:
        raise ConnectionError('Błąd połączenia z bazą danych.')

    excel_df = handled_config.extract(excel_path)
    excel_df = handled_config.transform(excel_df)

    result_df = db_df.merge(
        excel_df,
        left_on='Supplier_Code',
        right_on='code_pricelist',
        how='left'
    )

    result_df['price_pricelist'] = (result_df['price_pricelist'] * result_df['Factor'].fillna(1).astype(float)).fillna(0)
    result_df['price_diff'] = ((result_df['price_pricelist'] - result_df[config.currency_name])
                                /result_df[config.currency_name].replace(0, float('nan')))
    
    # strips the margin column of PCUE% characters (Margins in our database are stored like: ex. C80% = CZK 80%)
    result_df['Margin'] = result_df['Margin'].str.replace(r'[PCUE%]', '', regex=True).astype(float)/100
    result_df['new_price_PLN'] = round(result_df['price_pricelist'] * (1 + result_df['Margin']) * config.exchange, 2).fillna(0)

    result_df.to_excel(f'outputs/{handled_config.yaml_data.supplier_code}_output.xlsx', index=False)


if __name__ == '__main__':
    setup_logging()
    logger.info("Pipeline started")

    for cfg in Path('configs').glob('*.yaml'):
        logger.info("Pipeline %s started", cfg.name)
        config = YamlHandler(cfg)
        try:
            run_pipeline(config, config.file_path)
        except Exception:
            logger.exception("Pipeline %s failed", cfg.name)
            continue
        logger.info("Pipeline %s finished", cfg.name)
    logger.info("Pipeline finished")


