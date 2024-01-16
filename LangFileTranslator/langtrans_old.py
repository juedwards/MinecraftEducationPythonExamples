import requests
import openai
from openai import Client

def fetch_api_key(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text.strip()  # Returns the API key, removing any leading/trailing whitespace
    except requests.RequestException as e:
        print(f"Error fetching the API key: {e}")
        return None

# URL of the config file containing the API key
config_url = "https://meedownloads.blob.core.windows.net/learning-experience/ChatGPT/config.txt"
openai_api_key = fetch_api_key(config_url)

if openai_api_key:
    print("API key successfully retrieved.")
    client = Client(api_key=openai_api_key)  # Instantiate the client
else:
    print("Failed to retrieve the API key.")
    exit(1)  # Exit if the API key is not retrieved

openai.api_key = openai_api_key

def translate_text(text, target_language):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": f"Translate the following English text to {target_language}:"},
                      {"role": "user", "content": text}]
        )

        # Accessing the translated text from the response
        if response.choices:
            translated_text = response.choices[0].message.content.strip()
            return translated_text
        else:
            return None
    
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def translate_file(file_path, target_language):
    translated_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if '=' in line and '###' in line:
                text_to_translate = line.split('=')[1].split('###')[0].strip()
                translated_text = translate_text(text_to_translate, target_language)
                translated_lines.append(line.replace(text_to_translate, translated_text))
            else:
                translated_lines.append(line)
    return translated_lines
    
print(translate_text("Hello, how are you?", "Spanish"))
