# Minecraft Education PDF to Markdown Converter

This script allows you to convert PDF files into Markdown format. It uses the PyMuPDF library for PDF parsing and the markdownify library for converting text to Markdown.

## Features

- Cleans up the extracted text by removing extra whitespaces and multiple newlines.
- Converts the cleaned text to Markdown format.
- Automatically retrieves the publication date from the PDF metadata.
- Handles PDF filenames with invalid characters by sanitizing them.

## Installation

Before using the PDF to Markdown Converter, make sure to install the required Python packages. You can do this using `pip` and the provided `requirements.txt` file.

1. Clone or download the repository to your computer.

2. Open a command prompt or terminal and navigate to the directory containing the script and `requirements.txt` file.

3. Run the following command to install the required packages:

```bash
pip install -r requirements.txt

## Usage

To convert PDF files to Markdown, follow these steps:

1. Run the script by executing the main Python script, e.g., `pdf-to-md.py`.

2. The application window will open, allowing you to select input and output folders.

3. Click the "Browse" button next to "Select Input Folder" to choose the folder containing your PDF files.

4. Click the "Browse" button next to "Select Output Folder" to specify the folder where the generated Markdown files should be saved.

5. Click the "Convert PDF to MD" button to start the conversion process. The script will convert all PDF files in the input folder and save the resulting Markdown files in the output folder.

6. The progress label will indicate when the conversion is completed.
