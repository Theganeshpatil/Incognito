# INCOGNITO - IMAGE STEGANOGRAPHY TOOL

## Description
Incognito is a Python-based steganography tool that allows users to hide secret messages within images using the Least Significant Bit (LSB) encoding technique. The tool provides a simple graphical interface for embedding messages into images and extracting hidden messages from steganographic images.

## Features
- User-friendly graphical interface
- Embed text messages in images using LSB steganography  
- Extract hidden messages from steganographic images
- Support for common image formats (PNG, JPG, JPEG, BMP)
- Minimal visual impact on carrier images
- Error handling and validation
- Real-time feedback on operations

## Technical Details
The tool uses the Least Significant Bit (LSB) steganography technique, which works by:
- Converting the secret message into binary
- Replacing the least significant bit of each color channel (RGB) in the image pixels
- Using a special end marker to identify where the hidden message ends
- Preserving image quality while hiding information

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

## Installation
1. Create and activate a virtual environment:

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
    ```
    **macOS/Linux:** 

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2. Install required dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    

## Usage

1. Start the application:
    
    ```bash
    python -m src.main
    ```
    
2. To embed a message:
    - Click "Browse" to select an input image
    - Enter your secret message in the text area
    - Click "Embed Message"
    - Choose a location to save the output image
    - Wait for confirmation
3. To extract a message:
    - Click "Browse" to select an image with a hidden message
    - Click "Extract Message"
    - The hidden message will appear in the text area

## Project Structure

```bash
steganography_tool/
├── src/
│   ├── __init__.py
│   ├── steganography.py  # Core steganography functions
│   ├── gui.py           # GUI implementation
│   └── main.py          # Application entry point
├── tests/
│   └── __init__.py
├── images/              # Sample images directory
├── requirements.txt     # Project dependencies
└── README.txt          # Project documentation

```

## Limitations

- The size of the message that can be embedded depends on the image dimensions
- The output image must be saved in PNG format to prevent compression losses
- The tool currently supports text messages only
- Some image manipulations (like heavy compression) may corrupt the hidden message

## Security Considerations

- This tool is for educational purposes and does not provide cryptographic security
- The hidden messages are not encrypted by default
- The presence of a message can be detected by statistical analysis
- For sensitive information, consider adding encryption before embedding

## Support

For issues or questions, please contact the development team.

```vbnet
This markdown version should work well for documentation in a GitHub repository or similar platforms. Let me know if you need further adjustments
```