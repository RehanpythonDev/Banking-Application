# data_handler.py
import os
import json

class DataHandler:
    def __init__(self, file_path="bank_data.json"):
        """Initialize data handler with file path"""
        self.file_path = file_path
        
    def load_data(self):
        """Load account data from JSON file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            else:
                return {}
        except (json.JSONDecodeError, IOError):
            # Return empty dict if file is empty, corrupted, or can't be accessed
            return {}
            
    def save_data(self, data):
        """Save account data to JSON file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except IOError:
            print("Error: Unable to save data.")
            return False