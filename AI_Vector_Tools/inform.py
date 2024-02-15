import requests
from bs4 import BeautifulSoup
import os
import re

def save_webpage_text(url, output_path):
    # Make a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract all the visible text from the webpage
    visible_text = ""
    for element in soup.find_all(string=True):  # Use 'string' instead of 'text'
        if element.parent.name not in ["style", "script", "head", "title", "meta", "[document]"]:
            visible_text += element.strip() + "\n"

    # Remove empty lines from the visible text
    visible_text = "\n".join(line for line in visible_text.split("\n") if line.strip())

    # Save the text to the specified output path
    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, "w") as file:
        file.write(visible_text.strip())

    # Check if the MD file exceeds 64000 characters
    if len(visible_text.strip()) > 64000:
        print("The MD file exceeds 64000 characters.")
        # Ask the user if they want to split the file
        split_file = input("Do you want to split the file? (yes/no): ")
        if split_file.lower() == "yes":
            # Split the file into chunks of 64000 characters
            chunks = [visible_text[i:i + 64000] for i in range(0, len(visible_text), 64000)]

            # Save each chunk as a separate MD file
            for i, chunk in enumerate(chunks):
                split_md_file_path = os.path.join(os.path.expanduser("~"), "Downloads", f"output_part_{i+1}.md")
                with open(split_md_file_path, "w") as file:
                    file.write(chunk)

            print(f"The file has been split into {len(chunks)} parts.")
            # Print the individual locations of the split files
            for i, chunk in enumerate(chunks):
                print(f"Part {i+1} saved to: {os.path.join(os.path.expanduser('~'), 'Downloads', f'output_part_{i+1}.md')}")
    else:
        print("The MD file does not exceed 64000 characters.")
        print(f"MD file saved to: {output_path}")

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[\/:*?"<>|]', '_', filename)

#find all the links on a website and built a list of them
def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return links

# Example call     
url = input("Enter the URL of the website to covert: ")
links = get_all_links(url)

for link in links:
    if link:
        if link.startswith("http") or link.startswith("https"):
            filename = link.split("/")[-1]
            sanitized_filename = sanitize_filename(filename)  # Sanitize the filename
            output_path = os.path.join(os.path.expanduser("~"), "Downloads", f"{sanitized_filename}.md")
            save_webpage_text(url, output_path)
        else:
            print(f"Skipping invalid link: {link}")