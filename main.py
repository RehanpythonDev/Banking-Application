# main.py
import os
import sys
import getpass
import time
from datetime import datetime
from bank_account import BankAccount
from transaction import Transaction
from data_manager import DataManager
from authentication import Authentication
import msvcrt  # Add this import at the top with other imports

class BankingApp:
    def __init__(self):
        """Initialize the banking application"""
        self.data_manager = DataManager('bank_data.json')
        self.auth = Authentication()
        self.accounts = self.data_manager.load_data()
        self.current_user = None
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display the app header"""
        self.clear_screen()
        print("\n" + "=" * 50)
        print(" " * 15 + "BANKING APPLICATION")
        print("=" * 50 + "\n")
    
    def main_menu(self):
        """Display the main menu and handle user interaction"""
        while True:
            self.display_header()
            print("1. Create New Account")
            print("2. Log into Existing Account")
            print("3. Exit")
            
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                
                if choice == 1:
                    self.create_account()
                elif choice == 2:
                    self.login()
                elif choice == 3:
                    print("\nThank you for using the Banking Application! Goodbye.")
                    sys.exit(0)
                else:
                    print("\nInvalid choice. Please enter a number between 1 and 3.")
                    input("Press Enter to continue...")
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                input("Press Enter to continue...")
    
    def get_input(self, prompt, allow_back=True):
        """Get input from user with backspace functionality"""
        print(prompt, end='', flush=True)
        result = ''
        while True:
            char = msvcrt.getch()
            if char == b'\r':  # Enter key
                print()  # New line
                return result
            elif char == b'\x08':  # Backspace key
                if allow_back and not result:  # If input is empty and backspace is pressed
                    print("\nGoing back to previous menu...")
                    return None
                elif result:  # If there's text to delete
                    result = result[:-1]
                    print('\b \b', end='', flush=True)  # Erase character
            elif char.isalnum() or char in [b'.', b'$']:  # Allow numbers, letters, and some symbols
                char_str = char.decode('utf-8')
                result += char_str
                print(char_str, end='', flush=True)

    def create_account(self):
        """Handle account creation process"""
        self.display_header()
        print("CREATE NEW ACCOUNT\n")
        
        username = self.get_input("Enter username: ")
        if username is None:
            return
        username = username.strip().capitalize()
        
        # Check if username already exists
        if username in self.accounts:
            print(f"\nUsername '{username}' is already taken. Please choose another one.")
            input("Press Enter to continue...")
            return
        
        password = self.get_input("Enter password: ")
        if password is None:
            return
        
        try:
            deposit_str = self.get_input("Enter initial deposit amount: $")
            if deposit_str is None:
                return
            initial_deposit = float(deposit_str)
            if initial_deposit < 0:
                print("\nInitial deposit cannot be negative.")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("\nInvalid amount. Please enter a valid number.")
            input("Press Enter to continue...")
            return
        
        # Create new account without PIN first
        hashed_password = self.auth.hash_password(password)
        new_account = BankAccount(username, hashed_password, initial_deposit)
        
        # Save initial transaction if there's an initial deposit
        if initial_deposit > 0:
            transaction = Transaction(
                "deposit",
                initial_deposit,
                f"Initial deposit for account creation",
                initial_deposit
            )
            new_account.add_transaction(transaction)
        
        print(f"\nAccount for '{username}' created successfully with an initial balance of ${initial_deposit:.2f}!")
        print("\nNow let's set up your PIN for transactions.\n")
        
        # Ask for PIN setup after account creation
        while True:
            pin = input("Set a 4-digit PIN for transactions: ")
            if not pin.isdigit() or len(pin) != 4:
                print("\nInvalid PIN. Please enter a 4-digit numeric PIN.")
                continue
            
            # Confirm PIN
            confirm_pin = input("Confirm your PIN: ")
            if pin != confirm_pin:
                print("\nPINs do not match. Please try again.")
                continue
            
            new_account.pin = pin
            break
        
        # Save account to data store
        self.accounts[username] = new_account.to_dict()
        self.data_manager.save_data(self.accounts)
        
        print("\nPIN set successfully!")
        input("Press Enter to continue...")
    
    def login(self):
        """Handle user login process"""
        self.display_header()
        print("LOGIN TO EXISTING ACCOUNT\n")
        
        username = self.get_input("Enter username: ")
        if username is None:
            return
        username = username.strip()
        
        if username not in self.accounts:
            print("\nUsername not found.")
            print("1. Try again")
            print("2. Forgot Password")
            print("3. Back to Main Menu")
            
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice == 1:
                    return self.login()
                elif choice == 2:
                    return self.forgot_password()
                else:
                    return
            except ValueError:
                return
        
        password = self.get_input("Enter password: ")
        if password is None:
            return
        
        stored_password_hash = self.accounts[username]["password_hash"]
        if not self.auth.verify_password(password, stored_password_hash):
            print("\nIncorrect password.")
            print("1. Try again")
            print("2. Forgot Password")
            print("3. Back to Main Menu")
            
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice == 1:
                    return self.login()
                elif choice == 2:
                    return self.forgot_password()
                else:
                    return
            except ValueError:
                return
        
        print("\nLogin successful!")
        time.sleep(1)
        self.current_user = username
        self.account_menu()
    
    def account_menu(self):
        """Display the account menu after successful login"""
        while True:
            # Load the most current account data
            account_data = self.accounts[self.current_user]
            account = BankAccount.from_dict(account_data)
            
            self.display_header()
            print(f"Welcome, {self.current_user}!")
            print(f"Current Balance: ${account.balance:.2f}\n")
            
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Send Money")
            print("4. View Transaction History")
            print("5. Change PIN")
            print("6. Logout")
            
            try:
                choice = int(input("\nEnter your choice (1-6): "))
                
                if choice == 1:
                    self.deposit(account)
                elif choice == 2:
                    self.withdraw(account)
                elif choice == 3:
                    self.send_money(account)
                elif choice == 4:
                    self.view_transactions(account)
                elif choice == 5:
                    self.change_pin(account)
                elif choice == 6:
                    self.current_user = None
                    print("\nLogged out successfully.")
                    time.sleep(1)
                    return
                else:
                    print("\nInvalid choice. Please enter a number between 1 and 6.")
                    input("Press Enter to continue...")
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                input("Press Enter to continue...")
    
    def deposit(self, account):
        """Handle deposit operation"""
        self.display_header()
        print("DEPOSIT MONEY\n")
        print(f"Current Balance: ${account.balance:.2f}\n")
        
        if not self.verify_pin(account):
            return
        
        try:
            amount_str = self.get_input("Enter amount to deposit: $")
            if amount_str is None:
                return
            amount = float(amount_str)
            if amount <= 0:
                print("\nDeposit amount must be positive.")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("\nInvalid amount. Please enter a valid number.")
            input("Press Enter to continue...")
            return
        
        description = self.get_input("Enter a description (optional): ")
        if description is None:
            return
        
        # Update account balance and add transaction
        new_balance = account.balance + amount
        transaction = Transaction(
            "deposit",
            amount,
            description or "Deposit",
            new_balance
        )
        
        account.balance = new_balance
        account.add_transaction(transaction)
        
        # Save to data store
        self.accounts[self.current_user] = account.to_dict()
        self.data_manager.save_data(self.accounts)
        
        print(f"\n${amount:.2f} deposited successfully. New balance: ${new_balance:.2f}")
        input("Press Enter to continue...")
    
    def withdraw(self, account):
        """Handle withdrawal operation"""
        self.display_header()
        print("WITHDRAW MONEY\n")
        print(f"Current Balance: ${account.balance:.2f}\n")
        
        if not self.verify_pin(account):
            return
        
        try:
            amount_str = self.get_input("Enter amount to withdraw: $")
            if amount_str is None:
                return
            amount = float(amount_str)
            if amount <= 0:
                print("\nWithdrawal amount must be positive.")
                input("Press Enter to continue...")
                return
            
            if amount > account.balance:
                print(f"\nInsufficient funds. Your current balance is ${account.balance:.2f}")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("\nInvalid amount. Please enter a valid number.")
            input("Press Enter to continue...")
            return
        
        # Update account balance and add transaction
        new_balance = account.balance - amount
        transaction = Transaction(
            "withdrawal",
            amount,
            input("Enter a description (optional): ") or "Withdrawal",
            new_balance
        )
        
        account.balance = new_balance
        account.add_transaction(transaction)
        
        # Save to data store
        self.accounts[self.current_user] = account.to_dict()
        self.data_manager.save_data(self.accounts)
        
        print(f"\n${amount:.2f} withdrawn successfully. New balance: ${new_balance:.2f}")
        input("Press Enter to continue...")
    
    def send_money(self, sender_account):
        """Handle sending money to another account"""
        self.display_header()
        print("SEND MONEY\n")
        print(f"Current Balance: ${sender_account.balance:.2f}\n")
        
        recipient_username = self.get_input("Enter recipient's username: ")
        if recipient_username is None:
            return
        
        # Check if recipient exists
        if recipient_username not in self.accounts:
            print(f"\nRecipient '{recipient_username}' not found.")
            input("Press Enter to continue...")
            return
            
        # Can't send money to yourself
        if recipient_username == self.current_user:
            print("\nYou cannot send money to yourself.")
            input("Press Enter to continue...")
            return
        
        # Get amount to send
        try:
            amount_str = self.get_input("Enter amount to send: $")
            if amount_str is None:
                return
            amount = float(amount_str)
            if amount <= 0:
                print("\nAmount must be positive.")
                input("Press Enter to continue...")
                return
            
            if amount > sender_account.balance:
                print(f"\nInsufficient funds. Your current balance is ${sender_account.balance:.2f}")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("\nInvalid amount. Please enter a valid number.")
            input("Press Enter to continue...")
            return
        
        description = self.get_input("Enter a description (optional): ")
        if description is None:
            return

        # Verify PIN at the end before completing transaction
        if not self.verify_pin(sender_account):
            return
        
        # Update sender's account
        sender_new_balance = sender_account.balance - amount
        sender_transaction = Transaction(
            "transfer_out",
            amount,
            f"Sent to {recipient_username}: {description}",
            sender_new_balance
        )
        
        sender_account.balance = sender_new_balance
        sender_account.add_transaction(sender_transaction)
        
        # Update recipient's account
        recipient_data = self.accounts[recipient_username]
        recipient_account = BankAccount.from_dict(recipient_data)
        recipient_new_balance = recipient_account.balance + amount
        recipient_transaction = Transaction(
            "transfer_in",
            amount,
            f"Received from {self.current_user}: {description}",
            recipient_new_balance
        )
        
        recipient_account.balance = recipient_new_balance
        recipient_account.add_transaction(recipient_transaction)
        
        # Save both accounts to data store
        self.accounts[self.current_user] = sender_account.to_dict()
        self.accounts[recipient_username] = recipient_account.to_dict()
        self.data_manager.save_data(self.accounts)
        
        print(f"\n${amount:.2f} sent successfully to {recipient_username}.")
        print(f"Your new balance: ${sender_new_balance:.2f}")
        input("Press Enter to continue...")
    
    def view_transactions(self, account):
        """Display transaction history"""
        self.display_header()
        print("TRANSACTION HISTORY\n")
        
        transactions = account.transactions
        
        if not transactions:
            print("No transactions found.")
            input("Press Enter to continue...")
            return
        
        print(f"{'Type':<12} {'Amount':<10} {'Balance':<10} {'Date & Time':<20} {'Description':<30}")
        print("-" * 82)
        
        for transaction in transactions:
            # Format the transaction type for display
            type_display = transaction['type'].capitalize()
            if transaction['type'] == "transfer_in":
                type_display = "Received"
            elif transaction['type'] == "transfer_out":
                type_display = "Sent"
            
            print(f"{type_display:<12} ${transaction['amount']:<9.2f} ${transaction['balance']:<9.2f} {transaction['timestamp']:<20} {transaction['description']:<30}")
        
        input("\nPress Enter to continue...")

    def verify_pin(self, account):
        """Verify the user's PIN before proceeding with a transaction"""
        # Check if PIN exists and is saved in the account data
        if not hasattr(account, 'pin') or account.pin is None:
            print("\nYour account doesn't have a PIN set up.")
            print("Please set up a PIN first.\n")
            
            while True:
                pin = input("Set a 4-digit PIN for transactions: ")
                if not pin.isdigit() or len(pin) != 4:
                    print("\nInvalid PIN. Please enter a 4-digit numeric PIN.")
                    continue
                
                # Confirm PIN
                confirm_pin = input("Confirm your PIN: ")
                if pin != confirm_pin:
                    print("\nPINs do not match. Please try again.")
                    continue
                
                # Save PIN to account and persist to storage
                account.pin = pin
                self.accounts[self.current_user] = account.to_dict()
                self.data_manager.save_data(self.accounts)
                print("\nPIN set successfully!")
                break
        
        # Verify the PIN
        pin = self.get_input("Enter your 4-digit PIN to approve the transaction: ")
        if pin is None:
            return False
        if pin != account.pin:
            print("\nIncorrect PIN. Transaction denied.")
            input("Press Enter to continue...")
            return False
        return True

    def forgot_password(self):
        """Handle password reset process"""
        self.display_header()
        print("PASSWORD RESET\n")
        
        username = self.get_input("Enter username: ")
        if username is None:
            return
        username = username.strip()
        
        if username not in self.accounts:
            print("\nUsername not found.")
            input("Press Enter to continue...")
            return
        
        # Load account and check if PIN exists
        account = BankAccount.from_dict(self.accounts[username])
        
        if not hasattr(account, 'pin'):
            print("\nYour account doesn't have a PIN set up.")
            print("Please set up a PIN first.\n")
            
            while True:
                pin = input("Set a 4-digit PIN for transactions: ")
                if not pin.isdigit() or len(pin) != 4:
                    print("\nInvalid PIN. Please enter a 4-digit numeric PIN.")
                    continue
                
                # Confirm PIN
                confirm_pin = input("Confirm your PIN: ")
                if pin != confirm_pin:
                    print("\nPINs do not match. Please try again.")
                    continue
                
                account.pin = pin
                self.accounts[username] = account.to_dict()
                self.data_manager.save_data(self.accounts)
                print("\nPIN set successfully!")
                break
        
        # Now verify identity using PIN
        print("\nTo verify your identity, please enter your transaction PIN.")
        attempts = 3
        while attempts > 0:
            pin = self.get_input("Enter your 4-digit PIN: ")
            if pin is None:
                return
            
            if pin == account.pin:
                # Set new password
                while True:
                    new_password = self.get_input("\nEnter new password: ")
                    if new_password is None:
                        return
                    
                    confirm_password = self.get_input("Confirm new password: ")
                    if confirm_password is None:
                        return
                    
                    if new_password == confirm_password:
                        # Update password in account
                        hashed_password = self.auth.hash_password(new_password)
                        self.accounts[username]["password_hash"] = hashed_password
                        self.data_manager.save_data(self.accounts)
                        
                        print("\nPassword reset successful!")
                        input("Press Enter to continue...")
                        return
                    else:
                        print("\nPasswords do not match. Please try again.")
                
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"\nIncorrect PIN. {attempts} attempts remaining.")
                else:
                    print("\nToo many incorrect attempts. Please try again later.")
                    input("Press Enter to continue...")
                    return

    def change_pin(self, account):
        """Handle PIN change process"""
        self.display_header()
        print("CHANGE PIN\n")
        
        # First try with current PIN
        current_pin = self.get_input("Enter current PIN: ")
        if current_pin is None:
            return
        
        if not hasattr(account, 'pin') or current_pin != account.pin:
            print("\nIncorrect PIN.")
            print("1. Try again")
            print("2. Verify with password")
            print("3. Back to menu")
            
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice == 1:
                    return self.change_pin(account)
                elif choice == 2:
                    # Verify with password
                    password = self.get_input("\nEnter your password: ")
                    if password is None:
                        return
                    
                    stored_password_hash = self.accounts[self.current_user]["password_hash"]
                    if not self.auth.verify_password(password, stored_password_hash):
                        print("\nIncorrect password.")
                        input("Press Enter to continue...")
                        return
                    
                    # If password is correct, proceed with new PIN
                    while True:
                        new_pin = self.get_input("\nEnter new 4-digit PIN: ")
                        if new_pin is None:
                            return
                        
                        if not new_pin.isdigit() or len(new_pin) != 4:
                            print("\nInvalid PIN. Please enter a 4-digit numeric PIN.")
                            continue
                        
                        confirm_pin = self.get_input("Confirm new PIN: ")
                        if confirm_pin is None:
                            return
                        
                        if new_pin != confirm_pin:
                            print("\nPINs do not match. Please try again.")
                            continue
                        
                        # Save new PIN
                        account.pin = new_pin
                        self.accounts[self.current_user] = account.to_dict()
                        self.data_manager.save_data(self.accounts)
                        
                        print("\nPIN changed successfully!")
                        input("Press Enter to continue...")
                        return  # Return after successful PIN change
                else:
                    return
            except ValueError:
                return
        
        # Set new PIN
        while True:
            new_pin = self.get_input("\nEnter new 4-digit PIN: ")
            if new_pin is None:
                return
            
            if not new_pin.isdigit() or len(new_pin) != 4:
                print("\nInvalid PIN. Please enter a 4-digit numeric PIN.")
                continue
            
            confirm_pin = self.get_input("Confirm new PIN: ")
            if confirm_pin is None:
                return
            
            if new_pin != confirm_pin:
                print("\nPINs do not match. Please try again.")
                continue
            
            # Save new PIN
            account.pin = new_pin
            self.accounts[self.current_user] = account.to_dict()
            self.data_manager.save_data(self.accounts)
            
            print("\nPIN changed successfully!")
            input("Press Enter to continue...")
            break

def main():
    app = BankingApp()
    app.main_menu()

if __name__ == "__main__":
    main()