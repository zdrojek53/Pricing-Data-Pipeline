import yaml
from pathlib import Path


class YamlHandler:
    CURRENCY_KEYS = {
        'CZK': (7, 'Cena_CZK'),
        'USD': (8, 'Cena_USD'),
        'PLN': (9, 'Cena_PLN'),
        'EUR': (10, 'Cena_EUR')
    }

    def __init__(self, config_path: str | Path):
        with open(config_path) as f:
            self.data = yaml.safe_load(f)
        try:
            self.currency_id, self.currency_name = self.CURRENCY_KEYS[self.data['currency']]
            self.supplier_code = self.data['supplier_code']
            self.file_type = self.data['file_type']
            self.file_path = self.data['file_path']
        except KeyError:
            raise ValueError(f"Config {config_path} zawiera błędny klucz")


    