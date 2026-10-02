import yaml
from pathlib import Path


class YamlHandler:
    # numbers 7, 8, 9, 10 correspond to our values in database
    CURRENCY_KEYS = {
        'CZK': (7, 'Cena_CZK'),
        'USD': (8, 'Cena_USD'),
        'PLN': (9, 'Cena_PLN'),
        'EUR': (10, 'Cena_EUR')
    }

    def __init__(self, config_path: Path):
        try:
            with open(config_path, encoding="utf-8") as f:
                self.data = yaml.safe_load(f)
            self.currency_id, self.currency_name = self.CURRENCY_KEYS[self.data['currency']]
            self.supplier_code = self.data['supplier_code']
            self.file_type = self.data['file_type']
            self.file_path = self.data['file_path']
            self.exchange = self.data['exchange_rate']
        except KeyError:
            raise ValueError(f"Config {config_path} contains incorrect key")
        except TypeError:
            raise TypeError(f"Config {config_path} is empty or of wrong type")

