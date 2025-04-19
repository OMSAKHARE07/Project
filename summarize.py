from transformers import BartTokenizer, BartForConditionalGeneration
from pathlib import Path
import os
import re

# Use relative paths
EXTRACTED_FOLDER = "extract"
SUMMARY_FOLDER = "summary"

# Define model path
model_path = os.path.abspath("fine-tuned-legal-t5")
print(f"Loading model from: {model_path}")

# Load model and tokenizer separately from generation
try:
    tokenizer = BartTokenizer.from_pretrained(model_path, local_files_only=True)
    model = BartForConditionalGeneration.from_pretrained(model_path, local_files_only=True)
    print("Successfully loaded fine-tuned model!")
except Exception as e:
    print(f"Error loading fine-tuned model: {e}")
    print("Falling back to pre-trained model...")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def summarize_text_file(file_name: str) -> str:
    """Generate a high-quality summary using BART"""
    input_path = Path(EXTRACTED_FOLDER) / file_name
    output_path = Path(SUMMARY_FOLDER) / f"{Path(file_name).stem}_summary.txt"
    
    # Ensure summary folder exists
    os.makedirs(SUMMARY_FOLDER, exist_ok=True)
    
    try:
        # Read the input file
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # Clean text (remove formatting artifacts)
        text = re.sub(r'_{3,}', ' ', text)  # Remove repeated underscores
        text = re.sub(r'\.{3,}', '...', text)  # Normalize ellipses
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        # Process with BART
        inputs = tokenizer(text, max_length=1024, return_tensors="pt", truncation=True)
        
        # Generate summary with explicit parameters
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=200,
            min_length=50,
            length_penalty=2.0,
            early_stopping=True,  # Explicitly set to True
            no_repeat_ngram_size=3,
            repetition_penalty=1.5
        )
        
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        # Write the summary to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return str(output_path)
    
    except Exception as e:
        print(f"Error summarizing {file_name}: {str(e)}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Error generating summary: {str(e)}")
        return str(output_path)