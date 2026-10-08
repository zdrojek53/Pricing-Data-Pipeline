import logging
from logging_config import setup_logging


logger = logging.getLogger(__name__)
setup_logging()


def parse_margin(margin_column, config):
    """
    strips the margin column of PCUE% characters
    Margins in our database are stored like: ex. C80% = CZK 80%
    """
    try:
        margin_column = margin_column.astype(str).str.replace(r'[PCUE%]', '', regex=True)
        return margin_column.fillna(0).astype(float)/100
    except ValueError:
        logger.exception("Invalid margin values in database for %s.", config.name)



def transform_result(result_df, config):
    result_df['price_pricelist_new'] = (result_df['price_pricelist'] * result_df['Factor'].fillna(1).astype(float)).fillna(0)
    result_df['price_diff'] = ((result_df['price_pricelist_new'] - result_df[config.currency_name])
                                    /result_df[config.currency_name].replace(0, float('nan')))
    result_df['Margin'] = parse_margin(result_df['Margin'], config)
    result_df['new_price_PLN'] = round(result_df['price_pricelist_new'] * (1 + result_df['Margin']) * config.exchange, 2).fillna(0)

    return result_df

