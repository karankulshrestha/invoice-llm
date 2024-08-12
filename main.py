# main.py
import streamlit as st

from utils import extract_text_from_pdf, extract_text_from_image, generate_invoice
import tempfile

def main():
    st.title("Invoice Extraction App")

    st.sidebar.title("Upload File")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF or an image file", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Create a temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name
        
        if uploaded_file.type == "application/pdf":
            st.write("Processing PDF...")
            extracted_text = extract_text_from_pdf(temp_path)
        else:
            st.write("Processing Image...")
            extracted_text = extract_text_from_image(temp_path)
        
        st.write("Extracted Text:")
        st.text_area("Extracted Text", extracted_text, height=300)
        
        st.write("Generating Invoice Details...")
        invoice_details = generate_invoice(extracted_text)
        
        st.write("Extracted Invoice Details:")
        st.json(invoice_details)

if __name__ == "__main__":
    main()
