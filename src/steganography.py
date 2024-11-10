import cv2
import numpy as np
from typing import Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class SteganographyTool:
    END_MARKER = '1111111111111110'  # 16-bit marker to indicate end of message
    
    def __init__(self):
        """Initialize the encryption key"""
        self.salt = os.urandom(16)
        
    def generate_key(self, password: str) -> bytes:
        """Generate encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_message(self, message: str, password: str) -> bytes:
        """Encrypt the message using Fernet symmetric encryption"""
        key = self.generate_key(password)
        f = Fernet(key)
        return f.encrypt(message.encode())
    
    def decrypt_message(self, encrypted_message: bytes, password: str) -> str:
        """Decrypt the message using Fernet symmetric encryption"""
        try:
            key = self.generate_key(password)
            f = Fernet(key)
            decrypted_message = f.decrypt(encrypted_message)
            return decrypted_message.decode()
        except Exception as e:
            raise ValueError("Invalid password or corrupted message")
    
    @staticmethod
    def text_to_binary(text: bytes) -> str:
        """Convert bytes to binary string"""
        return ''.join(format(b, '08b') for b in text)
    
    @staticmethod
    def binary_to_bytes(binary: str) -> bytes:
        """Convert binary string back to bytes"""
        return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    
    def embed_message(self, image_path: str, message: str, password: str, output_path: str) -> Tuple[bool, str]:
        """Embed an encrypted message into an image using LSB steganography"""
        try:
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                return False, "Failed to load image"
            
            # Encrypt the message
            encrypted_message = self.encrypt_message(message, password)
            
            # Convert encrypted message to binary and add salt + end marker
            binary_message = self.text_to_binary(self.salt + encrypted_message) + self.END_MARKER
            
            # Check if message can fit in image
            if len(binary_message) > image.shape[0] * image.shape[1] * 3:
                return False, "Message too large for this image"
            
            data_index = 0
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    for color in range(3):  # RGB channels
                        if data_index < len(binary_message):
                            # Clear the LSB and set it to the message bit
                            image[i, j, color] = (image[i, j, color] & 0xFE) | int(binary_message[data_index])
                            data_index += 1
                        else:
                            break
            
            # Save the modified image
            cv2.imwrite(output_path, image)
            return True, "Message embedded successfully"
            
        except Exception as e:
            return False, f"Error embedding message: {str(e)}"
    
    def extract_message(self, image_path: str, password: str) -> Tuple[bool, str]:
        """Extract and decrypt a hidden message from an image"""
        try:
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                return False, "Failed to load image"
            
            binary_message = ""
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    for color in range(3):
                        # Extract LSB
                        binary_message += str(image[i, j, color] & 1)
                        
                        # Check for end marker
                        if len(binary_message) >= len(self.END_MARKER):
                            if binary_message[-len(self.END_MARKER):] == self.END_MARKER:
                                # Remove end marker and convert to bytes
                                message_bytes = self.binary_to_bytes(binary_message[:-len(self.END_MARKER)])
                                # Extract salt and encrypted message
                                self.salt = message_bytes[:16]
                                encrypted_message = message_bytes[16:]
                                # Decrypt the message
                                try:
                                    message = self.decrypt_message(encrypted_message, password)
                                    return True, message
                                except ValueError:
                                    return False, "Invalid password or corrupted message"
            
            return False, "No hidden message found"
            
        except Exception as e:
            return False, f"Error extracting message: {str(e)}" 