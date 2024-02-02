import os
import re
import fitz  # Import PyMuPDF
from markdownify import markdownify
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime  # Import datetime module

# Function to clean up text
def clean_text(text):
    # Remove extra whitespaces and tabs
    text = ' '.join(text.split())
    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n', text, flags=re.MULTILINE)
    # Find and replace "Minecraft Education Edition" or "Minecraft: Education Edition" with "Minecraft Education"
    text = re.sub(r'Minecraft\s*:?(\s*Education\s*Edition)?', 'Minecraft Education', text, flags=re.IGNORECASE)
    return text

def sanitize_filename(filename):
    # Replace characters not allowed in filenames with underscores
    invalid_chars = '\\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def pdf_to_md(pdf_path, output_folder):
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

    # Set the publication date to today's date
    publication_date = datetime.now().strftime('%Y-%m-%d')

    # Get the PDF metadata
    pdf_metadata = pdf_document.metadata

    title = pdf_metadata.get("title")
    if not title:
        title = os.path.splitext(os.path.basename(pdf_path))[0][:10]  # Use the first 10 characters of the PDF file name

    # Sanitize the title to create a valid filename
    sanitized_title = sanitize_filename(title)

    md_file_name = f"{publication_date}_{sanitized_title}.md"
    md_file_path = os.path.join(output_folder, md_file_name)

    # Save as a Markdown file
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)


def select_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, input_folder)

def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, output_folder)

def convert_pdf_to_md():
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

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_to_md(pdf_path, output_folder)

    progress_label.config(text="Conversion completed.")
    messagebox.showinfo("Info", "PDF to MD conversion completed.")

# Function to exit the application
def exit_app():
    root.destroy()

# Create a tkinter window
root = tk.Tk()
root.title("PDF to MD Converter")
root.geometry("400x400")

# Styling
root.configure(bg="#F0F0F0")
root.option_add("*Font", "Arial 12")

# Input folder label and entry
input_folder_label = tk.Label(root, text="Select Input Folder:", bg="#F0F0F0")
input_folder_label.pack(pady=10)
input_folder_entry = tk.Entry(root, width=30)
input_folder_entry.pack()
input_folder_button = tk.Button(root, text="Browse", command=select_input_folder)
input_folder_button.pack(pady=5)

# Output folder label and entry
output_folder_label = tk.Label(root, text="Select Output Folder:", bg="#F0F0F0")
output_folder_label.pack(pady=10)
output_folder_entry = tk.Entry(root, width=30)
output_folder_entry.pack()
output_folder_button = tk.Button(root, text="Browse", command=select_output_folder)
output_folder_button.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert PDF to MD", command=convert_pdf_to_md, bg="#4CAF50", fg="white")
convert_button.pack(pady=20)

# Progress label
progress_label = tk.Label(root, text="", bg="#F0F0F0")
progress_label.pack()

exit_button = tk.Button(root, text="Exit", command=exit_app, bg="#F44336", fg="white")
exit_button.pack(pady=10)

# Start the tkinter main loop
root.mainloop()
