

def parse_margin(margin_column):
    return margin_column.str.replace(r'[PCUE%]', '', regex=True).astype(float)/100


def transform_result(result_df, config):
    result_df['price_pricelist'] = (result_df['price_pricelist'] * result_df['Factor'].fillna(1).astype(float)).fillna(0)
    result_df['price_diff'] = ((result_df['price_pricelist'] - result_df[config.currency_name])
                                    /result_df[config.currency_name].replace(0, float('nan')))
        
    # strips the margin column of PCUE% characters (Margins in our database are stored like: ex. C80% = CZK 80%)
    result_df['Margin'] = parse_margin(result_df['Margin'])
    result_df['new_price_PLN'] = round(result_df['price_pricelist'] * (1 + result_df['Margin']) * config.exchange, 2).fillna(0)

    return result_df