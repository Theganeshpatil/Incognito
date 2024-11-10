import cv2
import numpy as np
from typing import Tuple

class SteganographyTool:
    END_MARKER = '1111111111111110'  # 16-bit marker to indicate end of message
    
    @staticmethod
    def text_to_binary(text: str) -> str:
        """Convert text message to binary string"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def binary_to_text(binary: str) -> str:
        """Convert binary string back to text"""
        message = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            message += chr(int(byte, 2))
        return message
    
    def embed_message(self, image_path: str, message: str, output_path: str) -> Tuple[bool, str]:
        """Embed a message into an image using LSB steganography"""
        try:
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                return False, "Failed to load image"
            
            # Convert message to binary and add end marker
            binary_message = self.text_to_binary(message) + self.END_MARKER
            
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
    
    def extract_message(self, image_path: str) -> Tuple[bool, str]:
        """Extract a hidden message from an image"""
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
                                # Remove end marker and convert to text
                                message = self.binary_to_text(binary_message[:-len(self.END_MARKER)])
                                return True, message
            
            return False, "No hidden message found"
            
        except Exception as e:
            return False, f"Error extracting message: {str(e)}" 