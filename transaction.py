# transaction.py
from datetime import datetime

class Transaction:
    def __init__(self, transaction_type, amount, description, balance_after):
        """
        Initialize a transaction
        
        Args:
            transaction_type (str): Type of transaction ('deposit' or 'withdrawal')
            amount (float): Amount of money involved
            description (str): Description of the transaction
            balance_after (float): Account balance after the transaction
        """
        self.transaction_type = transaction_type
        self.amount = float(amount)
        self.description = description
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.balance = float(balance_after)
    
    def to_dict(self):
        """Convert the transaction to a dictionary for storage"""
        return {
            'type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'timestamp': self.timestamp,
            'balance': self.balance
        }