# File Upload and Text Extraction App

This FastAPI application allows users to upload files (Images, PDFs, and Word documents) and extract text from them using OCR (Optical Character Recognition) and text-processing libraries.

## 🚀 Features

- Upload Images (`.jpg`, `.jpeg`, `.png`, `.webp`)
- Upload PDFs (`.pdf`)
- Upload Word Documents (`.doc`, `.docx`)
- Extract text from the uploaded files
- Save extracted text as `.txt` files

## ⚙️ Requirements

- Python 3.12+
- Tesseract OCR (Installed and configured)

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/project.git
   cd project

   ```

2. Install dependencies:
   pip install -r requirements.txt

3. Make sure Tesseract OCR is installed:
   Download from Tesseract OCR.
   Add the Tesseract path to the system environment variables or specify it in the code:

   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

🚀 Run the Application

uvicorn app:app --reload
