
from typing import List
from ....domain.interfaces.account import IAccountOpeningUseCase, IAccountRepository, ICustomerRepository


class RequestNewAccountUseCase(IAccountOpeningUseCase):
    def __init__(self, account_repo:IAccountRepository):
        self.account_repo = account_repo

    def execute(self, customer_id: str, account_type: str):
        return self.account_repo.create_account(customer_id, account_type)

class InquiryAccountRequirementsUseCase(IAccountOpeningUseCase):
    def __init__(self, account_repo: IAccountRepository):
        self.account_repo = account_repo

    def execute(self, account_type: str) -> List[str]:
        return self.account_repo.get_requirements(account_type)

class AccountOpeningEligibilityUseCase(IAccountOpeningUseCase):
    def __init__(self, customer_repo: ICustomerRepository):
        self.customer_repo = customer_repo

    def execute(self, customer_id: str) -> bool:
        return self.customer_repo.check_eligibility(customer_id)
