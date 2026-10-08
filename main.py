import logging
from logging_config import setup_logging
from db_extraction.extract_db_data import fetch_db_data
from adapters.excel_adapter import ExcelAdapter
from yaml_handler import YamlHandler
from pathlib import Path
from dotenv import load_dotenv
from output_handler import transform_result


load_dotenv()
logger = logging.getLogger(__name__)


def run_pipeline(config: YamlHandler, excel_path: str) -> None:

    handled_config = ExcelAdapter(config.config)

    db_df = fetch_db_data(config)

    if db_df.empty:
        raise ConnectionError('Database connection error.')

    excel_df = handled_config.extract(excel_path)
    excel_df = handled_config.transform(excel_df)

    result_df = db_df.merge(
        excel_df,
        left_on='Supplier_Code',
        right_on='code_pricelist',
        how='left'
    )

    result_df = transform_result(result_df, config)

    result_df.to_excel(f'outputs/{handled_config.yaml_data.supplier_code}_output.xlsx', index=False)


if __name__ == '__main__':
    setup_logging()
    logger.info("Pipeline started")

    for cfg in Path('configs').glob('*.yaml'):
        logger.info("Pipeline %s started", cfg.name)
        try:
            config = YamlHandler(cfg)
            run_pipeline(config, config.file_path)
        except Exception:
            logger.exception("Pipeline %s failed", cfg.name)
            continue
        logger.info("Pipeline %s finished", cfg.name)
    logger.info("Pipeline finished")


