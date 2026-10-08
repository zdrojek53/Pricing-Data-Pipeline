import pandas as pd
import logging
from adapters.base_adapter import BaseAdapter

class ExcelAdapter(BaseAdapter):

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data
        self.logger = logging.getLogger(__name__)


    def extract(self, path):
        self.logger.info("Loading pricelist: %s", path)
        try:
            df = pd.read_excel(
                                path, header=self.yaml_data.header_row,
                                usecols=lambda col: col in self.yaml_data.column_mapping,
                                sheet_name=self.yaml_data.sheet_name,
                                dtype={'code_pricelist': str}
                            ).rename(columns=self.yaml_data.column_mapping)
            self.logger.info("Loaded: %s", path)
            return df
        except FileNotFoundError:
            self.logger.exception("The file %s was not found. Verify the path.", path)
            raise
        except PermissionError:
            self.logger.exception("Unable to access %s. Make sure it is not open.", path)
            raise
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            self.logger.exception("Data on path %s is empty or corrupted.", path)
            raise
        except KeyError:
            self.logger.exception("Invalid YAML format")
            raise


    def transform(self, raw):
        try:
            original_len = len(raw)
            df = (
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
            dropped = original_len - len(df)
            if dropped:
                self.logger.info("Dropped %d rows", dropped)
            return df
        except KeyError:
            self.logger.exception("Wrong column mapping in YAML")
            raise

