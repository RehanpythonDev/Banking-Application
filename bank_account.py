# bank_account.py
from datetime import datetime

class BankAccount:
    def __init__(self, username, password_hash, initial_balance=0.0):
        """Initialize bank account with username, password hash, and initial balance"""
        self.username = username
        self.password_hash = password_hash
        self.balance = float(initial_balance)
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions = []
    
    @classmethod
    def from_dict(cls, data):
        """Create a BankAccount instance from a dictionary"""
        account = cls(
            data['username'],
            data['password_hash'],
            data['balance']
        )
        account.created_at = data['created_at']
        account.transactions = data.get('transactions', [])
        return account
    
    def to_dict(self):
        """Convert the account to a dictionary for storage"""
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'balance': self.balance,
            'created_at': self.created_at,
            'transactions': self.transactions
        }
    
    def add_transaction(self, transaction):
        """Add a transaction to the account history"""
        self.transactions.append(transaction.to_dict())