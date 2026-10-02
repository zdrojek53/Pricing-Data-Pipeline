import yaml
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typing import Literal


class YamlConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    currency: Literal["CZK", "PLN", "EUR", "USD"]
    supplier_code: str
    file_type: Literal["excel"]
    file_path: str
    exchange_rate: float
    sheet_name: str
    header_row: int
    column_mapping: dict



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
                data = yaml.safe_load(f)

            self.config = YamlConfig.model_validate(data)

        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {config_path}") from e

        self.currency_id, self.currency_name = self.CURRENCY_KEYS[self.config.currency]


    @property
    def supplier_code(self) -> str:
        return self.config.supplier_code

    @property
    def file_type(self) -> str:
        return self.config.file_type

    @property
    def file_path(self) -> str:
        return self.config.file_path

    @property
    def exchange(self) -> float:
        return self.config.exchange_rate

