from ...domain.interfaces.account import IAccountOpeningUseCase


class AccountOpeningController:
    def __init__(self, account_use_case: IAccountOpeningUseCase, customer_use_case: IAccountOpeningUseCase):
        self.account_use_case = account_use_case
        self.customer_use_case = customer_use_case

    def request_new_account(self, customer_id: str, account_type: str):
        return self.account_use_case.execute(customer_id, account_type)

    def inquiry_account_requirements(self, account_type: str):
        return self.account_use_case.execute(account_type)

    def check_eligibility(self, customer_id: str):
        return self.customer_use_case.execute(customer_id)