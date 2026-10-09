import logging
import pandas as pd
from logging_config import setup_logging


logger = logging.getLogger(__name__)
setup_logging()


def parse_margin(margin_column: pd.Series, config) -> pd.Series:
    """
    strips the margin column of PCUE% characters
    Margins in the database are stored like: ex. C80% = CZK 80%
    """

    try:
        margin_column = (margin_column.astype("string")
                         .str.replace(r'[PCUE%]', '', regex=True)
                         .str.replace(",", ".", regex=True))
        return pd.to_numeric(margin_column, errors="coerce").fillna(0)/100
    
    except ValueError:
        logger.exception("Invalid margin values in database for %s.", config.name)
        raise



def transform_result(result_df, config):
    result_df['price_pricelist_new'] = (result_df['price_pricelist'] * result_df['Factor'].fillna(1).astype(float)).fillna(0)
    result_df['price_diff'] = ((result_df['price_pricelist_new'] - result_df[config.currency_name])
                                    /result_df[config.currency_name].replace(0, float('nan')))
    result_df['Margin'] = parse_margin(result_df['Margin'], config)
    result_df['new_price_PLN'] = round(result_df['price_pricelist_new'] * (1 + result_df['Margin']) * config.exchange, 2).fillna(0)

    return result_df

