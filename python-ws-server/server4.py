import asyncio
import websockets
import json
import os
from uuid import uuid4
import openai 

openai.api_type = "azure"
openai.api_base = "https://dev-azure-ai-studio-aiservices1665690750.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Unique tag for identifying messages sent by the bot
BOT_TAG = "[ai]"
# Color to apply to text to see AI responses
SUPER_SCRIPT = "§e"

async def generate_gpt_response(message):
    prompt = {
        "role": "system",
        "content": f"Respond to the following message from a Minecraft Education player, making sure your language is suitable for age 9 and the response is always about Minecraft Education: {message}"
    }
    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo-Lorenzo-Test",
        messages=[prompt],  # Here, the prompt is wrapped in a list
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    output = completion.choices[0].message.content.strip()
    print("Copilot says: " + output)

    # Split the output into lines and append the BOT_TAG to each line, limiting to 5 lines
    return [SUPER_SCRIPT + line + " " + BOT_TAG for line in output.split('\n')[:20]]

async def process_message(json_message, websocket):
    try:
        message = json.loads(json_message) if not isinstance(json_message, dict) else json_message
    except TypeError as e:
        print(f"Error processing message: {e}")
        return

    print(message)
    body = message.get('body', {})
    header = message.get('header', {})
    msg_text = body.get('message', '')
    event_name = header.get('eventName', '')

    if event_name == 'PlayerMessage' and BOT_TAG not in msg_text:
        print(f"Received a message: {msg_text}")
        response_lines = await generate_gpt_response(msg_text)
        for line in response_lines:
            await send_message(line, websocket)
            # Sleep for a short time to avoid flooding the chat
            await asyncio.sleep(0.5)

async def send_message(message, websocket):
    command = {
        "body": {
            "origin": {"type": "player"},
            "commandLine": f"/say {message}",
            "version": 1
        },
        "header": {
            "requestId": str(uuid4()),
            "messagePurpose": "commandRequest",
            "version": 1,
            "messageType": "commandRequest"
        }
    }
    await websocket.send(json.dumps(command))

async def mineproxy(websocket, path):
    print('Connected')
    # Subscribe to PlayerMessage events and 
    await websocket.send(json.dumps({
        "header": {
            "version": 1,
            "requestId": str(uuid4()),
            "messageType": "commandRequest",
            "messagePurpose": "subscribe"
        },
        "body": {
            "eventName": "PlayerMessage"
        },
    }))

    try:
        # Listen for messages from Minecraft
        async for msg in websocket:
            await process_message(msg, websocket)
    except websockets.exceptions.ConnectionClosedError:
        print('Disconnected from Minecraft')

async def start_server():
    server = await websockets.serve(mineproxy, "localhost", 3000)
    print('Server started. On Minecraft, type /connect localhost:3000')
    await server.wait_closed()

asyncio.run(start_server())
