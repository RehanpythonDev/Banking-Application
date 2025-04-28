# banking_system.py
import datetime
from data_handler import DataHandler
from utils import hash_password

class BankingSystem:
    def __init__(self):
        self.data_handler = DataHandler()
        self.accounts = self.data_handler.load_data()
        
    def create_account(self, username, password, initial_deposit=0.0):
        """Create a new bank account"""
        hashed_password = hash_password(password)
        
        # Initialize account structure
        account = {
            "username": username,
            "password": hashed_password,
            "balance": initial_deposit,
            "transactions": []
        }
        
        # Add initial deposit transaction if amount > 0
        if initial_deposit > 0:
            transaction = {
                "type": "DEPOSIT",
                "amount": initial_deposit,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "balance": initial_deposit
            }
            account["transactions"].append(transaction)
        
        # Add account to accounts dictionary
        self.accounts[username] = account
        
        # Save updated accounts data
        self.data_handler.save_data(self.accounts)
        return True
        
    def account_exists(self, username):
        """Check if an account exists"""
        return username in self.accounts
        
    def authenticate(self, username, password):
        """Authenticate a user"""
        if not self.account_exists(username):
            return False
            
        hashed_password = hash_password(password)
        return self.accounts[username]["password"] == hashed_password
        
    def get_balance(self, username):
        """Get account balance"""
        if not self.account_exists(username):
            return None
            
        return self.accounts[username]["balance"]
        
    def deposit(self, username, amount):
        """Deposit money into an account"""
        if not self.account_exists(username):
            return False
            
        # Update balance
        self.accounts[username]["balance"] += amount
        current_balance = self.accounts[username]["balance"]
        
        # Record transaction
        transaction = {
            "type": "DEPOSIT",
            "amount": amount,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": current_balance
        }
        self.accounts[username]["transactions"].append(transaction)
        
        # Save updated accounts data
        self.data_handler.save_data(self.accounts)
        return True
        
    def withdraw(self, username, amount):
        """Withdraw money from an account"""
        if not self.account_exists(username):
            return False
            
        # Check if sufficient balance
        if self.accounts[username]["balance"] < amount:
            return False
            
        # Update balance
        self.accounts[username]["balance"] -= amount
        current_balance = self.accounts[username]["balance"]
        
        # Record transaction
        transaction = {
            "type": "WITHDRAW",
            "amount": amount,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": current_balance
        }
        self.accounts[username]["transactions"].append(transaction)
        
        # Save updated accounts data
        self.data_handler.save_data(self.accounts)
        return True
        
    def get_transaction_history(self, username):
        """Get transaction history for an account"""
        if not self.account_exists(username):
            return []
            
        return self.accounts[username]["transactions"]