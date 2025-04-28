# data_manager.py
import json
import os

class DataManager:
    def __init__(self, file_path):
        """Initialize data manager with the specified file path"""
        self.file_path = file_path
    
    def load_data(self):
        """Load account data from JSON file"""
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is empty or corrupted, return empty dict
            return {}
    
    def save_data(self, data):
        """Save account data to JSON file"""
        try:
            # Ensure data directory exists
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False