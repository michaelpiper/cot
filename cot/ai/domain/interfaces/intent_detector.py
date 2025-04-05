from abc import ABC, abstractmethod
from typing import Tuple


class IIntentDetector(ABC):
    @abstractmethod
    def predict(self, text:str)->Tuple[str, float]:...