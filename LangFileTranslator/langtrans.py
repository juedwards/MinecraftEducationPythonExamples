# Minecraft Education Lang File Translator using ChatGPT
# Justin Edwards
# Microsoft
# 2020-04-01
# v1.0.0

import openai
from openai import OpenAI
from openai import AsyncOpenAI
import asyncio
import requests
import sys

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

# Fetch the API key
openai_api_key = fetch_api_key(config_url)

# Check if the API key was successfully retrieved
if openai_api_key:
    print("API key successfully retrieved.")
    # Continue with your code, using the API key as needed
else:
    print("Failed to retrieve the API key.")
    sys.exit(1)  # Exit the script if the API key was not retrieved

#client = OpenAI(api_key=openai_api_key)

client = AsyncOpenAI(api_key=openai_api_key)

async def translate_text(text, target_language):
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # or the appropriate chat model
            messages=[{"role": "system", "content": f"Translate the following English text to {target_language}:"},
                      {"role": "user", "content": text}]
        )
        
        # Access the first choice and get the message content
        translated_text = response.choices[0].message['content'].strip()
        #print(type(response))
        #print(dir(response))

        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

async def translate_file(file_path, target_language):
    translated_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if '=' in line and '###' in line:
                text_to_translate = line.split('=')[1].split('###')[0].strip()
                translated_text = await translate_text(text_to_translate, target_language)
                if translated_text is not None:
                    new_line = line.replace(text_to_translate, translated_text)
                    translated_lines.append(new_line)
                    print(f"Translated line: {new_line}")
                else:
                    print(f"Failed to translate line: {line}")
                    translated_lines.append(line)  # Keep the original line
            else:
                translated_lines.append(line)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)  # Ensure this line has the closing parenthesis

async def main():
    # Set file path and language
    file_path = 'C:\\Users\\juedwards\\Downloads\\en_US_goo_game.lang'  # Change this to the path of your lang file
    language = 'Spanish'  # Change this to the language you want to translate to

    # Translate the file content
    await translate_file(file_path, language)
    print("Translation complete.")

if __name__ == "__main__":
    asyncio.run(main())