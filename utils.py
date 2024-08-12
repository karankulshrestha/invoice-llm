# utils.py
import fitz  # PyMuPDF
import os
from PIL import Image
import pytesseract
import time
from strictjson import strict_json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API Key is not set in the .env file")

# Set the OpenAI API Key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Configure Tesseract for Linux
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()
    return text

def extract_text_from_image(image_path):
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
    return text

def llm(system_prompt: str, user_prompt: str):
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model='gpt-4o',
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def generate_invoice(invoice_context):
    start_time = time.time()
    print(f"generate_invoice started at {start_time}")

    invoice_prompt = f"""
        **Task:**
        You are given text extracted from an invoice. Please extract the following details from the text:
        1. **Customer Details:** Name, Address, and Contact Information.
        2. **Products:** List of products including their names and quantities.
        3. **Total Amount:** The total amount on the invoice.
        **Extracted Text:**
        {invoice_context}
    """

    res = strict_json(
        system_prompt='You are an Invoice Analysis Expert',
        user_prompt=invoice_prompt,
        output_format={
            'customer': 'Name of the customer: str',
            'address': 'Address of the customer: str',
            'email': 'Email of the customer: str',
            'phone': 'Phone Number of the customer: int',
            'Products': 'List of the products: List[str]',
            'Amount': 'Total Amount in the invoice: int'
        },
        llm=llm
    )

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"generate_invoice execution time: {execution_time} seconds")

    return res
