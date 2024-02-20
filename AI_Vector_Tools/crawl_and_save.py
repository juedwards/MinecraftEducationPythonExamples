import requests
import os
from bs4 import BeautifulSoup
import re

def crawl_and_extract(domain):
    # Send a GET request to the domain
    response = requests.get(domain)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the links on the page
    links = soup.find_all('a')
    
    # Loop through each link
    for link in links:
        # Get the URL of the link
        url = link.get('href')
        
        # Check if the URL is not None and belongs to the same domain
        if url and domain in url:
            # Send a GET request to the URL
            response = requests.get(url)
            
            # Extract the HTML name from the URL
            html_name = url.split('/')[-1]
            
            # Remove any query parameters from the HTML name
            html_name = html_name.split('?')[0]
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the text from the page
            text = soup.get_text()
            
            # Clean the text by removing special characters and blank lines
            cleaned_text = re.sub(r'[^\w\s]', '', text)
            cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
            
            # Save the cleaned text as a Markdown file based on the HTML name
            file_name = html_name + '.md'
            file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)
            with open(file_path, 'a') as file:
                file.write(cleaned_text)
                file.write('\n---\n')

# Replace 'https://example.com' with the specific web domain you want to crawl
crawl_and_extract('https://educommunity.minecraft.net/')
