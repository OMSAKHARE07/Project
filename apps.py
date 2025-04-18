from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil, os, pytesseract
from PIL import Image
from pdfminer.high_level import extract_text as extract_pdf_text
import docx2txt
import win32com.client
from summarize import summarize_text_file  # import your summarize logic

# === FOLDER PATHS ===
BASE_DIR = r"C:\Users\Administrator\Music\Project\Project"
UPLOAD_FOLDER = os.path.join(BASE_DIR, "upload")
EXTRACTED_FOLDER = os.path.join(BASE_DIR, "extract")
SUMMARY_FOLDER = os.path.join(BASE_DIR, "summary")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === APP SETUP ===
app = FastAPI()
last_summary_filename = None

# === CORS FOR REACT ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ext = Path(file_path).suffix.lower()

    try:
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
        elif ext == ".pdf":
            text = extract_pdf_text(file_path)
        elif ext == ".docx":
            text = docx2txt.process(file_path)
        elif ext == ".doc":
            word = win32com.client.Dispatch("Word.Application")
            doc = word.Documents.Open(file_path)
            text = doc.Content.Text
            doc.Close()
            word.Quit()
        else:
            return JSONResponse(content={"message": "Unsupported file format."}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message": f"Extraction failed: {str(e)}"}, status_code=500)

    filename = Path(file.filename).stem + ".txt"
    text_path = os.path.join(EXTRACTED_FOLDER, filename)
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    global last_summary_filename
    last_summary_filename = filename

    return {"message": "File uploaded successfully!", "filename": filename}


@app.get("/summarize/{filename}")
async def summarize_file(filename: str):
    result = summarize_text_file(filename)
    return {"status": "success" if "saved" in result.lower() else "failed"}


@app.get("/api/result")
async def get_summary():
    if last_summary_filename:
        summary_path = os.path.join(SUMMARY_FOLDER, last_summary_filename)
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                return {"text": f.read()}
    return {"text": ""}
