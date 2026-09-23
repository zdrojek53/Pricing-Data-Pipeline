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
            self.currency_key = self.CURRENCY_KEYS[self.data['currency']]
        except KeyError:
            raise ValueError(f"Nieobsługiwana waluta w configu: {self.data.get('currency')}")


    