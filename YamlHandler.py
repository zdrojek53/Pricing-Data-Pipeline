import yaml
from pathlib import Path


class YamlHandler:
    currency_data = {
        'CZK': (7, 'Cena_CZK'),
        'USD': (8, 'Cena_USD'),
        'PLN': (9, 'Cena_PLN'),
        'EUR': (10, 'Cena_EUR')
    }

    with open(Path(__file__).resolve().parent / 'configs' / 'siot.yaml') as f:
        data = yaml.safe_load(f)
        currency_key = currency_data[data['currency']]


    