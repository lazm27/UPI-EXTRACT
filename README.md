# UPI Transaction Detail Extractor

## Overview

The UPI Transaction Detail Extractor is a Python application that utilizes OpenCV for image processing and Tesseract OCR for text recognition. It extracts transaction details such as the transaction status, amount, date, time, and UPI ID from UPI payment screenshots.

## Features

- Preprocesses images to enhance text recognition quality.
- Uses Tesseract OCR to extract text from processed images.
- Supports extracting amounts both numerically and in words.
- Provides structured output in JSON format for easy integration with other applications.

## Requirements

- Python 3.x
- OpenCV
- Pytesseract
- Tesseract-OCR
- NumPy
- JSON

## Installation

1. **Install Python**: Ensure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install Required Packages**: Use pip to install the required packages. You can run the following command:

   ```python
   pip install opencv-python pytesseract numpy
   ```

3. **Install Tesseract-OCR**: Download and install Tesseract-OCR from [Tesseract's GitHub repository](https://github.com/tesseract-ocr/tesseract). 

   Make sure to add the Tesseract installation path to your system's environment variables.

4. **Configure Pytesseract**: Update the Tesseract path in the code to match your installation:

   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## Usage

1. **Prepare Your Image**: Save your UPI payment screenshot as a JPG or PNG file.

2. **Update the Image Path**: In the code, update the `image_path` variable to point to your saved image:

   ```python
   image_path = 'images/upi_image.jpg'  # Image path
   ```

3. **Run the Script**: Execute the script to extract transaction details:

   ```bash
   python main.py
   ```

4. **View Output**: The extracted transaction details will be printed in JSON format to the console.

## Code Structure

- **text_to_number_with_decimal**: Converts text representations of numbers (including decimal amounts) to numeric format.
- **preprocess_image**: Applies image processing techniques to enhance text visibility for OCR.
- **clean_extracted_text**: Cleans up common OCR misreads in the extracted text.
- **extract_transaction_details**: The main function that orchestrates the extraction process and outputs structured transaction details in JSON format.

## Example Output

```json
{
    "transaction_status": "Success",
    "amount": "240.7",
    "date": "25 Sep 2024",
    "time": "12:30 PM",
    "UPI ID": "example@upi"
}
```

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
```

