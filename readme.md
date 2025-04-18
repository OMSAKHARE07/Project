# Validease

This FastAPI application allows users to upload files (Images, PDFs, and Word documents) and extract text from them using OCR (Optical Character Recognition) and text-processing libraries.

## 🚀 Features

- Upload Images (`.jpg`, `.jpeg`, `.png`, `.webp`)
- Upload PDFs (`.pdf`)
- Upload Word Documents (`.doc`, `.docx`)
- Extract text from the uploaded files
- Save extracted text as `.txt` files

## ⚙️ Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pytesseract
- Pillow
- pdfminer.six
- python-docx (docx2txt)
- pywin32 (for `.doc` handling)
- transformers
- torch

### 🌐 Frontend (React)

- Node.js 14+
- npm or yarn


## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OMSAKHARE07/Project.git
   cd project

   ```

2. Install dependencies:
   ``` bash
      pip install -r requirements.txt
   ```
   
3. Make sure Tesseract OCR is installed:
   Download from Tesseract OCR.
   Add the Tesseract path to the system environment variables or specify it in the code:

   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

4. Install required files as
   ``` bash
   pip install fastapi uvicorn pytesseract Pillow pdfminer.six python-docx pywin32 transformers torch
   ```
   
5. Start the backend using 
  ``` bash 
   uvicorn apps:app --reload
 ```
6. Start front end by
   ``` bash
   cd my-app
   npm install
   npm start
```
9. Go to the Locahost: 3000 port.
