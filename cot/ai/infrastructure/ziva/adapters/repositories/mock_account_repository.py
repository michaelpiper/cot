from typing import List
from .....domain.entities.account import Account, Customer
from .....domain.interfaces.account import IAccountRepository, ICustomerRepository


class MockAccountRepository(IAccountRepository):
    def __init__(self):
        self.accounts = {}
        self.requirements = {
            "savings": ["ID proof", "Address proof"],
            "checking": ["ID proof", "Income proof"],
            "fixed_deposit": ["ID proof", "Initial deposit"]
        }

    def create_account(self, customer_id: str, account_type: str) -> Account:
        account_id = f"acc_{len(self.accounts) + 1}"
        account = Account(account_id=account_id, account_type=account_type, status="pending", customer_id=customer_id)
        self.accounts[account_id] = account
        return account

    def get_requirements(self, account_type: str) -> List[str]:
        return self.requirements.get(account_type, [])

    def get_status(self, account_id: str) -> str:
        return self.accounts.get(account_id, {}).get("status", "unknown")

class MockCustomerRepository(ICustomerRepository):
    def __init__(self):
        self.customers = {
            "cust_1": Customer(customer_id="cust_1", name="John Doe", eligibility=True),
            "cust_2": Customer(customer_id="cust_2", name="Jane Smith", eligibility=False)
        }

    def check_eligibility(self, customer_id: str) -> bool:
        return self.customers.get(customer_id, {}).eligibility

    def get_documents(self, customer_id: str) -> List[str]:
        return self.customers.get(customer_id, {}).documents or []