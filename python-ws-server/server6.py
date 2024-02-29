import asyncio
import websockets
import json
import os
from uuid import uuid4
from datetime import datetime
import openai

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
#openai.api_key = os.getenv("AZURE_OPEN_API_KEY")

# Unique tag for AI responses and script setup
BOT_TAG = "[ai]"
SUPER_SCRIPT = "§e"

# Events to subscribe to, for logging
INTERESTING_EVENTS = [
    "PlayerMessage",
    "PlayerTravelled",
    "PlayerTransform",
    "PlayerTeleported",
    "BlockBroken",
    "BlockPlaced",
    "ItemAcquired",
    "ItemCrafted",
    "ItemDestroyed",
    "ItemDropped",
    "ItemEnchanted",
    "ItemSmelted",
    "ItemUsed"
]

# Log file setup based on current datetime
session_start_time = datetime.now().strftime("%d%m%y%H%M")
log_file_name = f"{session_start_time}.json"

async def generate_gpt_response(message):
    # Function to generate response from Azure's GPT instance
    prompt = {
        "role": "system",
        "content": f"Respond to the following message from a Minecraft Education player, making sure your language is suitable for age 9: {message}"
    }
    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo-Lorenzo-Test",
        messages=[prompt],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    output = completion.choices[0].message.content.strip()

    return [SUPER_SCRIPT + line + " " + BOT_TAG for line in output.split('\n')[:20]]

async def log_event(json_message):
    # Function to log events to a JSON file
    try:
        message = json.loads(json_message) if not isinstance(json_message, dict) else json_message
    except TypeError as e:
        print(f"Error processing message: {e}")
        return

    with open(log_file_name, "a") as log_file:
        log_file.write(json.dumps(message) + "\n")

async def send_message(player_name, message, websocket):
    # Send a private message to a specific player using the /tell command
    command = {
        "body": {
            "origin": {"type": "player"},
            "commandLine": f"/tell {player_name} {message}",
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

async def perform_analysis(player_name):
    # Function to count the number of entries for a given player
    data = []
    with open(log_file_name, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {line}\nError: {e}")

    player_reports = {}

    for event in data:
        # Ensure the 'eventName' key exists in the 'header' dictionary
        if 'eventName' in event.get('header', {}):
            eventName = event['header']['eventName']
            if player_name not in player_reports:
                player_reports[player_name] = {'distance_traveled': 0, 'blocks_broken': 0, 'blocks_placed': 0}
            if eventName == 'PlayerTravelled':
                player_reports[player_name]['distance_traveled'] += event['body']['metersTravelled']
            elif eventName == 'BlockBroken':
                player_reports[player_name]['blocks_broken'] += 1
            elif eventName == 'BlockPlaced':
                player_reports[player_name]['blocks_placed'] += 1

    report = f"Player Name: {player_name}\n"  # Start the report with the player's name
    for name, data in player_reports.items():
        # For each event, append the event name followed by the variable
        report += f"Distance Traveled: {data['distance_traveled']}\n"
        report += f"Blocks Broken: {data['blocks_broken']}\n"
        report += f"Blocks Placed: {data['blocks_placed']}\n"

    return report

async def process_message(json_message, websocket):
    # Process incoming messages for both chat and logging
    try:
        message = json.loads(json_message) if not isinstance(json_message, dict) else json_message
    except TypeError as e:
        print(f"Error processing message: {e}")
        return

    await log_event(json_message)  # Log every message

    body = message.get('body', {})
    header = message.get('header', {})
    msg_text = body.get('message', '')
    event_name = header.get('eventName', '')
    player_name = body.get('sender', '')  # Extracting player name

    if event_name == 'PlayerMessage' and BOT_TAG not in msg_text:
        if msg_text.strip() == '!Analyse':
            analysis = await perform_analysis(player_name)
            await send_message(player_name, analysis, websocket)  # Send response to the player
        else:
            response_lines = await generate_gpt_response(msg_text)
            for line in response_lines:
                await send_message(player_name, line, websocket)  # Send response to the player
                await asyncio.sleep(0.5)  # To avoid flooding


async def subscribe_to_events(websocket):
    # Subscribe to all interesting events for logging
    for event_name in INTERESTING_EVENTS:
        await websocket.send(json.dumps({
            "header": {
                "version": 1,
                "requestId": str(uuid4()),
                "messageType": "commandRequest",
                "messagePurpose": "subscribe"
            },
            "body": {
                "eventName": event_name
            },
        }))

async def mineproxy(websocket, path):
    # Main proxy function to handle connections
    print('Connected to Minecraft')
    await subscribe_to_events(websocket)

    try:
        async for msg in websocket:
            await process_message(msg, websocket)
    except websockets.exceptions.ConnectionClosedError:
        print('Disconnected from Minecraft')

async def start_server():
    # Start the websocket server
    print(f'Server starting, logging to {log_file_name}...')
    server = await websockets.serve(mineproxy, "localhost", 3000)
    print('Server started. On Minecraft, type /connect localhost:3000')
    await server.wait_closed()

# Run the server
asyncio.run(start_server())
