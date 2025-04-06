from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from pathlib import Path
import pytesseract
from PIL import Image
from pdfminer.high_level import extract_text as extract_pdf_text
import docx2txt
import win32com.client  # For .doc file handling

app = FastAPI()

# Folder paths
UPLOAD_FOLDER = r"C:\Users\Administrator\Desktop\Project\upload"
EXTRACTED_FOLDER = r"C:\Users\Administrator\Desktop\Project\extract"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Route to serve index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())

# Function to save uploaded files
def save_file(file: UploadFile, folder: str) -> str:
    file_path = os.path.join(folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

# Function to extract text
def extract_text(file_path: str) -> str:
    file_ext = Path(file_path).suffix.lower()
    extracted_text = ""

    if file_ext in [".jpg", ".jpeg", ".png", ".webp"]:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
    elif file_ext == ".pdf":
        extracted_text = extract_pdf_text(file_path)
    elif file_ext == ".docx":
        extracted_text = docx2txt.process(file_path)
    elif file_ext == ".doc":
        # Handling .doc files using win32com
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        extracted_text = doc.Content.Text
        doc.Close()
        word.Quit()
    else:
        extracted_text = "Unsupported file format."

    # Save extracted text
    text_filename = os.path.join(EXTRACTED_FOLDER, Path(file_path).stem + ".txt")
    with open(text_filename, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    return f"Text extracted and saved to {text_filename}"

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = save_file(file, UPLOAD_FOLDER)
    result = extract_text(file_path)
    return {"message": result}
