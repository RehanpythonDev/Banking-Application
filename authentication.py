# authentication.py
import hashlib
import os
import base64

class Authentication:
    def __init__(self):
        """Initialize authentication system"""
        # Salt length for password hashing
        self.salt_length = 16
    
    def hash_password(self, password):
        """
        Create a secure hash of the password using SHA-256 with a random salt
        
        Args:
            password (str): The plaintext password to hash
            
        Returns:
            str: The salt and hash combined as a base64 string
        """
        # Generate a random salt
        salt = os.urandom(self.salt_length)
        
        # Hash the password with the salt
        hash_obj = hashlib.sha256()
        hash_obj.update(salt)
        hash_obj.update(password.encode('utf-8'))
        password_hash = hash_obj.digest()
        
        # Combine salt and hash, and convert to base64 for storage
        salted_hash = salt + password_hash
        encoded_hash = base64.b64encode(salted_hash).decode('utf-8')
        
        return encoded_hash
    
    def verify_password(self, password, stored_hash):
        """
        Verify a password against a stored hash
        
        Args:
            password (str): The plaintext password to verify
            stored_hash (str): The stored hash to check against
            
        Returns:
            bool: True if the password matches, False otherwise
        """
        try:
            # Decode the stored hash
            decoded = base64.b64decode(stored_hash.encode('utf-8'))
            
            # Extract salt (first self.salt_length bytes)
            salt = decoded[:self.salt_length]
            
            # Hash the input password with the same salt
            hash_obj = hashlib.sha256()
            hash_obj.update(salt)
            hash_obj.update(password.encode('utf-8'))
            input_hash = hash_obj.digest()
            
            # Extract the original hash (everything after the salt)
            original_hash = decoded[self.salt_length:]
            
            # Compare the computed hash with the stored hash
            return input_hash == original_hash
            
        except Exception:
            # If any error occurs during verification, return False
            return False