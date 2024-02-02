import os
import re
import fitz  # PyMuPDF
from markdownify import markdownify as md
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

# Function to clean up text
def clean_text(text):
    text = ' '.join(text.split())
    text = re.sub(r'\n\s*\n', '\n', text, flags=re.MULTILINE)
    text = re.sub(r'Minecraft\s*:?(\s*Education\s*Edition)?', 'Minecraft Education', text, flags=re.IGNORECASE)
    return text

# Function to sanitize filenames
def sanitize_filename(filename):
    invalid_chars = '\\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

# Function to split MD files if they exceed 65,000 characters
def split_md_files(output_folder):
    md_files = [file for file in os.listdir(output_folder) if file.endswith('.md')]
    
    for md_file in md_files:
        md_file_path = os.path.join(output_folder, md_file)
        with open(md_file_path, 'r', encoding='utf-8') as original_file:
            content = original_file.read()
        
        if len(content) > 65000:
            chunks = [content[i:i + 65000] for i in range(0, len(content), 65000)]
            base_name, extension = os.path.splitext(md_file)
            for i, chunk in enumerate(chunks):
                split_md_file_path = os.path.join(output_folder, f"{base_name}_part_{i+1}{extension}")
                with open(split_md_file_path, 'w', encoding='utf-8') as split_file:
                    split_file.write(chunk)
            os.remove(md_file_path)

# Function to convert a single PDF to Markdown
def pdf_to_md(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    extracted_text = ''
    for page in pdf_document:
        extracted_text += page.get_text()
    pdf_document.close()

    cleaned_text = clean_text(extracted_text)
    md_content = md(cleaned_text)

    publication_date = datetime.now().strftime('%Y-%m-%d')
    pdf_metadata = pdf_document.metadata
    title = pdf_metadata.get("title", os.path.splitext(os.path.basename(pdf_path))[0][:10])
    sanitized_title = sanitize_filename(title)

    md_file_name = f"{publication_date}_{sanitized_title}.md"
    md_file_path = os.path.join(output_folder, md_file_name)
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

# Function to handle folder selection and entry updates
def select_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, input_folder)

def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, output_folder)

# Function to convert all PDFs in the selected folder to Markdown
def convert_pdf_to_md_gui():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()

    if not os.path.exists(input_folder):
        messagebox.showerror("Error", "Input folder does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [pdf_file for pdf_file in os.listdir(input_folder) if pdf_file.endswith('.pdf')]

    if not pdf_files:
        messagebox.showinfo("Info", "No PDF files found in the input folder.")
        return

    progress_label.config(text="Converting PDFs...")

    max_logical_cores = multiprocessing.cpu_count()
    max_workers = max(1, int(2/3 * max_logical_cores))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_folder, pdf_file)
            executor.submit(pdf_to_md, pdf_path, output_folder)

    split_md_files(output_folder)

    progress_label.config(text="Conversion completed.")
    messagebox.showinfo("Info", "PDF to MD conversion completed.")

# Function to exit the application
def exit_app():
    root.destroy()

# Create the GUI
root = tk.Tk()
root.title("PDF to MD Converter")
root.geometry("400x400")
root.configure(bg="#F0F0F0")
root.option_add("*Font", "Arial 12")