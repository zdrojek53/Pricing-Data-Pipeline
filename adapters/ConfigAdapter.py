import yaml
import pandas as pd
import MainAdapter

class ConfigAdapter(MainAdapter.MainAdapter):
    supplier_code: str

    def extract(self, path):
        return pd.read_excel(path, usecols=['Code', 'Net price'])

    def transform(self, raw):
        raw = (
        raw.dropna(subset=['Code'])
        .fillna({'Net price': 0})
        .drop_duplicates(subset=['Code'])
        .assign(Code = lambda x: x['Code'].astype('str').str.strip())
        .assign(**{'Net price': (lambda x: x['Net price'].astype('float64'))})
        )

        return raw