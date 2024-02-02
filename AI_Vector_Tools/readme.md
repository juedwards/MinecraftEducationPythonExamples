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
