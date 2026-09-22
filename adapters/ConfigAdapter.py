import pandas as pd
from adapters.MainAdapter import MainAdapter

class ConfigAdapter(MainAdapter):

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data


    def extract(self, path):
        print(self.yaml_data)
        return pd.read_excel(path, usecols=[self.yaml_data['column_mapping']['code_pricelist']
                                            , self.yaml_data['column_mapping']['price_pricelist']])

    def transform(self, raw):
        raw = (
        raw.dropna(subset=['Code'])
        .fillna({'Net price': 0})
        .drop_duplicates(subset=['Code'])
        .assign(Code = lambda x: x['Code'].astype('str').str.strip())
        .assign(**{'Net price': (lambda x: x['Net price'].astype('float64'))})
        )

        return raw

    