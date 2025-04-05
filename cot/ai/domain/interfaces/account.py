from abc import ABC, abstractmethod
from typing import List
from ..entities.account import Account

# Similarly, define other use cases...
class IAccountRepository(ABC):
    @abstractmethod
    def create_account(self, customer_id: str, account_type: str) -> Account:
        pass

    @abstractmethod
    def get_requirements(self, account_type: str) -> List[str]:
        pass

    @abstractmethod
    def get_status(self, account_id: str) -> str:
        pass

class ICustomerRepository(ABC):
    @abstractmethod
    def check_eligibility(self, customer_id: str) -> bool:
        pass

    @abstractmethod
    def get_documents(self, customer_id: str) -> List[str]:
        pass
    
class IAccountOpeningUseCase(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass