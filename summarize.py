from transformers import BartTokenizer, BartForConditionalGeneration
from pathlib import Path
import os

BASE_DIR = r"C:\Users\Administrator\Music\Project\Project"
EXTRACTED_FOLDER = os.path.join(BASE_DIR, "extract")
SUMMARY_FOLDER = os.path.join(BASE_DIR, "summary")

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def chunk_text(text, max_tokens=1024):
    tokens = tokenizer.tokenize(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i + max_tokens]
        chunks.append(tokenizer.convert_tokens_to_string(chunk))
    return chunks

def summarize_text_file(file_name: str) -> str:
    input_path = Path(EXTRACTED_FOLDER) / file_name
    output_path = Path(SUMMARY_FOLDER) / file_name

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    text_chunks = chunk_text(text)
    all_summaries = []

    for chunk in text_chunks:
        inputs = tokenizer(chunk, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            length_penalty=2.0,
            max_length=400,
            min_length=60,
            no_repeat_ngram_size=3,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        all_summaries.append(summary)

    full_summary = "\n\n".join(all_summaries)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_summary)

    return f"summary saved to {output_path}"
