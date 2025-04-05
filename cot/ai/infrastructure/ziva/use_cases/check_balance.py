class CheckAccountBalanceUseCase:
    def __init__(self,account_id) -> None:
        self.account_id = account_id

    def execute(self):
        return {
            "balance": "NGN 500,000.00"
        }