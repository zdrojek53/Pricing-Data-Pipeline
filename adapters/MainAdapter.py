from abc import ABC, abstractmethod
import pandas as pd

class MainAdapter(ABC):

    @abstractmethod
    def extract(self, path: str) -> pd.DataFrame:
        pass


    @abstractmethod
    def transform(self, raw: pd.DataFrame) -> pd.DataFrame:
        pass


