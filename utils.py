# utils.py
import os
import hashlib
import getpass

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def hash_password(password):
    """Create a SHA-256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def display_menu(options):
    """Display a menu with numbered options"""
    print("\nPlease select an option:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print()

def get_valid_input(prompt, valid_range):
    """Get valid input from user within a specified range"""
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_range:
                return choice
            else:
                print(f"Please enter a number between {min(valid_range)} and {max(valid_range)}.")
        except ValueError:
            print("Please enter a valid number.")