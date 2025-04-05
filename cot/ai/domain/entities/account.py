from dataclasses import dataclass
from typing import List

@dataclass
class Account:
    account_id: str
    account_type: str
    status: str  # e.g., "pending", "approved", "rejected"
    customer_id: str
    requirements: List[str] = None

@dataclass
class Customer:
    customer_id: str
    name: str
    eligibility: bool = False
    documents: List[str] = None