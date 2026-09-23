import pandas as pd
from adapters.MainAdapter import MainAdapter

class ConfigAdapter(MainAdapter):

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data


    def extract(self, path):
        try:
            return (pd.read_excel(
                                path, header=self.yaml_data['header_row'],
                                usecols=lambda col: col in self.yaml_data['column_mapping']
                            )
                    .rename(columns=self.yaml_data['column_mapping']))
        except Exception as e:
            print(e)
            return pd.DataFrame()
    

    def transform(self, raw):
        return (
            raw.assign(
                code_pricelist = lambda x: x['code_pricelist'].astype('str').str.strip(),
                price_pricelist = lambda x: pd.to_numeric(
                    x['price_pricelist'], errors='coerce'
                )
            )
            .dropna(subset=['code_pricelist'])
            .fillna({'price_pricelist': 0.0})
            .drop_duplicates(subset=['code_pricelist'])
        )

    