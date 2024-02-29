import asyncio
import os
import openai

BOT_TAG = "[ai]"

# Function to get the API key from a file
def get_api_key_from_file():
    api_key_path = os.path.join(os.path.expanduser('~'), 'OneDrive - Microsoft', 'Documents', 'Keys', 'open_api_key.txt')
    try:
        with open(api_key_path, 'r') as file:
            api_key = file.read().strip()  # Remove any leading/trailing whitespace
        return api_key
    except FileNotFoundError:
        print(f"API key file not found at {api_key_path}.")
        return None
    except Exception as e:
        print(f"Error reading API key file: {e}")
        return None

# Get the API key from the file
api_key = get_api_key_from_file()

# Use the API key if it was successfully retrieved
if api_key is not None:
    openai.api_key = api_key
else:
    print("Failed to retrieve API key. Please check the file and path.")
    exit()  # Exit the script if no API key is found

# Azure API setup
openai.api_type = "azure"
openai.api_base = "https://dev-azure-ai-studio-aiservices1665690750.openai.azure.com/"
openai.api_version = "2023-07-01-preview"

async def generate_gpt_response(messages):
    # Function to generate response from Azure's GPT instance
    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo-Lorenzo-Test",
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    output = completion.choices[0].message.content.strip()

    return [line + " " + BOT_TAG for line in output.split('\n')[:20]]

async def main():
    print("GPT Conversation CLI. Type 'exit' to end the conversation.\n")
    conversation_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Ending conversation.")
            break

        # Append the user's message to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        responses = await generate_gpt_response(conversation_history)
        for response in responses:
            print(response)

        # Append GPT's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})

# Run the main loop
if __name__ == "__main__":
    asyncio.run(main())
