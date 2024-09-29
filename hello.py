import cv2
import pytesseract
import re
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def text_to_number_with_decimal(text):
    # Define mappings for the number words
    units = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19
    }
    
    tens = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
    }

    scales = {
        "hundred": 100,
        "thousand": 1000,
        "million": 1_000_000,
        "billion": 1_000_000_000
    }

    words = text.lower().split()
    total = 0
    current = 0
    decimal_part = 0
    decimal_scale = 0

    for word in words:
        if word == "and":
            decimal_scale = 1  # Indicates that the next numbers are decimal
        elif word in units:
            if decimal_scale > 0:
                decimal_part += units[word] * (10 ** (-decimal_scale))
                decimal_scale += 1  # Increase the decimal scale for next digit
            else:
                current += units[word]
        elif word in tens:
            if decimal_scale > 0:
                decimal_part += tens[word] * (10 ** (-decimal_scale))
                decimal_scale += 1
            else:
                current += tens[word]
        elif word in scales:
            current *= scales[word]
            total += current
            current = 0

    # Correct the decimal part
    if decimal_scale > 0:
        decimal_part /= (10 ** (decimal_scale - 1))  # Adjust for decimal place

    return total + current + decimal_part

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filtering to reduce noise while keeping edges sharp
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    
    thr = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Apply adaptive thresholding for better text detection
    thresh = cv2.adaptiveThreshold(thr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Resize for better OCR performance
    scaled = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    
    return scaled

def clean_extracted_text(extracted_text):
    # Replace common OCR misreads
    #extracted_text = extracted_text.replace('~', '₹')  # Fix rupee sign
    #extracted_text = extracted_text.replace('@', '')    # Remove misplaced '@' characters
    extracted_text = extracted_text.replace('Paise', '')    # Remove misplaced '@' characters
    extracted_text = extracted_text.replace('QI PMT', 'PM')  # Clean misread of time information
    return extracted_text

def extract_transaction_details(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    
    # Tesseract config to improve accuracy (use --psm 6 for uniform blocks of text)
    #tesseract_config = r'--oem 3 --psm 6 -l eng+hin'  # Adding hindi for ₹ symbol if needed
    tesseract_config = r'--oem 3 --psm 6 -l eng+hin tessedit_char_whitelist=" ₹@0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:.,"'
    #tesseract_config = r'-l eng+hin'
    # Use Tesseract to extract text
    extracted_text = pytesseract.image_to_string(processed_image, config=tesseract_config)
    
    # Clean the extracted text
    extracted_text = clean_extracted_text(extracted_text)

    # Print extracted text (for debugging)
    print("Extracted Text:\n", extracted_text)

    # Determine transaction status
    transaction_status = "Success" if any(phrase in extracted_text.upper() for phrase in ["PAYMENT SUCCESSFUL", "MONEY SENT SUCCESSFULLY", "SUCCESS"]) else "Failed"
    
    # Extract amount
    amount_match = re.search(r'[₹Rs2]\s?([\d,.]+)', extracted_text)
    amount=amount_match.group(1)
    words_amount_match = re.search(r'Rupees\s+(.*?)(?=\s+Only)', extracted_text)
    #print(words_amount_match.group(1))

    if amount_match.group(1)=='0':

        amount=text_to_number_with_decimal(words_amount_match.group(1))
     
    # Extract time and date
    time_date_match = re.search(r'(\d{1,2}:\d{2} [APM]{2}),\s*(\d{1,2} \w{3} \d{4})', extracted_text)
    
    # Extract UPI ID
    upi_id_match = re.search(r'UPI ID:\s*([\w.-]+@[a-zA-Z]+)', extracted_text)


    # Create a structured JSON object
    transaction_details = {
        "transaction_status": transaction_status,
        "amount": amount,
        "date": time_date_match.group(2) if time_date_match else None,
        "time": time_date_match.group(1) if time_date_match else None,
        "UPI ID": upi_id_match.group(1) if upi_id_match else None
    }

    return transaction_details

# Example usage
image_path = 'images/upi_image.jpg'  # Image path
details = extract_transaction_details(image_path)

# Print structured details
print(json.dumps(details, indent=4))
