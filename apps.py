
import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pytesseract
from PIL import Image
from summarize import summarize_text_file  # your own summarize logic

# === FOLDER PATHS (Using relative paths for cross-platform compatibility) ===
UPLOAD_FOLDER = "upload"
EXTRACTED_FOLDER = "extract"
SUMMARY_FOLDER = "summary"

# === Create folders if they don't exist ===
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)

# === APP SETUP ===
app = FastAPI()
last_summary_filename = None

# === CORS FOR REACT ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === STATIC FILES ===
# Serve static files from the current directory
app.mount("/static", StaticFiles(directory="."), name="static")

# === ROUTES ===
@app.get("/")
async def read_index():
    # Check if index.html exists in current directory
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "API is running. Access /docs for API documentation."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ext = Path(file_path).suffix.lower()

    # Continue with your existing code...
    # Make sure to complete this section based on your original implementation
    return {"filename": file.filename, "path": file_path}

@app.get("/summarize/{filename}")
async def summarize_file(filename: str):
    """Process and summarize an uploaded file"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return {"error": f"File {filename} not found"}
    
    # Extract text based on file type
    ext = Path(file_path).suffix.lower()
    extracted_text_path = ""
    
    try:
        if ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"]:
            # Process image files
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            # Save extracted text
            extracted_text_path = os.path.join(EXTRACTED_FOLDER, f"{Path(filename).stem}.txt")
            with open(extracted_text_path, "w", encoding="utf-8") as f:
                f.write(text)
                
        elif ext in [".pdf", ".doc", ".docx", ".txt"]:
            # Extract text based on file type
            extracted_text_path = os.path.join(EXTRACTED_FOLDER, f"{Path(filename).stem}.txt")
            
            if ext == ".txt":
                shutil.copy(file_path, extracted_text_path)
            elif ext == ".pdf":
                from pdfminer.high_level import extract_text
                text = extract_text(file_path)
                with open(extracted_text_path, "w", encoding="utf-8") as f:
                    f.write(text)
            elif ext in [".doc", ".docx"]:
                import docx2txt
                text = docx2txt.process(file_path)
                with open(extracted_text_path, "w", encoding="utf-8") as f:
                    f.write(text)
        else:
            return {"error": f"Unsupported file type: {ext}"}
            
        # Summarize the extracted text - THIS IS WHERE WE USE summarize.py
        global last_summary_filename
        summary_path = summarize_text_file(os.path.basename(extracted_text_path))
        last_summary_filename = Path(summary_path).name
        
        return {"success": True, "filename": filename, "summary": last_summary_filename}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/result")
async def get_result():
    """Return the result of the last summarization"""
    global last_summary_filename
    
    if not last_summary_filename:
        return {"error": "No summary available. Process a file first."}
    
    summary_path = os.path.join(SUMMARY_FOLDER, last_summary_filename)
    
    if not os.path.exists(summary_path):
        return {"error": f"Summary file not found: {last_summary_filename}"}
    
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_text = f.read()
    
    return {
        "summary": summary_text,
        "filename": last_summary_filename
    }