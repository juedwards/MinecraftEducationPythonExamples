import os
import re
import fitz  # Import PyMuPDF
from markdownify import markdownify
from tqdm import tqdm  # Import tqdm for progress bar

# Function to clean up text
def clean_text(text):
    # Remove extra whitespaces and tabs
    text = ' '.join(text.split())
    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n', text, flags=re.MULTILINE)
    return text

# Function to convert PDF to MD
def pdf_to_md(pdf_path, md_path):
    # Open PDF file with PyMuPDF
    pdf_document = fitz.open(pdf_path)
    
    extracted_text = ''
    for page in pdf_document:
        extracted_text += page.get_text()
    
    pdf_document.close()

    # Clean up the extracted text
    cleaned_text = clean_text(extracted_text)

    # Convert cleaned text to Markdown
    md_content = markdownify(cleaned_text)

    # Save as a Markdown file
    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

# Specify the input and output directories
input_folder = r'C:\Users\juedwards\OneDrive - Microsoft\Research'
output_folder = r'C:\Users\juedwards\OneDrive - Microsoft\MD_files'

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List PDF files in the input directory
pdf_files = [pdf_file for pdf_file in os.listdir(input_folder) if pdf_file.endswith('.pdf')]

# Create a tqdm progress bar
progress_bar = tqdm(total=len(pdf_files), desc="Converting PDFs", unit="file")

# Iterate through PDF files in the input directory
for pdf_file in pdf_files:
    pdf_path = os.path.join(input_folder, pdf_file)
    md_file = os.path.splitext(pdf_file)[0] + '.md'
    md_path = os.path.join(output_folder, md_file)
    pdf_to_md(pdf_path, md_path)
    progress_bar.update(1)  # Update progress bar
    progress_bar.set_postfix(Completed=f"{progress_bar.n}/{progress_bar.total}", refresh=True)  # Update progress description

progress_bar.close()  # Close progress bar

print("Conversion completed.")
