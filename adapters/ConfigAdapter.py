import pandas as pd
from adapters.MainAdapter import MainAdapter

class ConfigAdapter(MainAdapter):

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data


    def extract(self, path):
        print(self.yaml_data)
        return (pd.read_excel(path, usecols=lambda col: col in self.yaml_data['column_mapping'])
                .rename(columns=self.yaml_data['column_mapping']))

    def transform(self, raw):
        raw = (
        raw.dropna(subset=['code_pricelist'])
        .fillna({'price_pricelist': 0})
        .drop_duplicates(subset=['code_pricelist'])
        .assign(code_pricelist = lambda x: x['code_pricelist'].astype('str').str.strip())
        .assign(price_pricelist = lambda x: x['price_pricelist'].astype('float64'))
        )

        return raw

    