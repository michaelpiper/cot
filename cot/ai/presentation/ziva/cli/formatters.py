# from rich.table import Table
# from core.entities import TransactionHistory

# def print_transactions(history: TransactionHistory) -> Table:
#     """Rich table formatting"""
#     table = Table(title="Transaction History")
#     table.add_column("Date", style="cyan")
#     table.add_column("Amount", justify="right")
    
#     for txn in history.transactions:
#         table.add_row(
#             txn.date.strftime("%Y-%m-%d"),
#             f"{txn.amount:.2f} {txn.currency}"
#         )
#     return table