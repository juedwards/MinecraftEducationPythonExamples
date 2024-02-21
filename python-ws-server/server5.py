import asyncio
import websockets
import json
from uuid import uuid4
from datetime import datetime

# Events to subscribe to, based on the JSON events gist provided
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
    # Add more event names as needed based on your interest
]

# Generate a file name based on the current date and time
session_start_time = datetime.now().strftime("%d%m%y%H%M")
log_file_name = f"{session_start_time}.json"

async def log_event(json_message):
    try:
        message = json.loads(json_message) if not isinstance(json_message, dict) else json_message
    except TypeError as e:
        print(f"Error processing message: {e}")
        return

    # Save the event to the session log file
    with open(log_file_name, "a") as log_file:
        log_file.write(json.dumps(message) + "\n")

async def subscribe_to_events(websocket):
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
    print('Connected to Minecraft')
    await subscribe_to_events(websocket)

    try:
        # Listen for messages from Minecraft
        async for msg in websocket:
            await log_event(msg)
    except websockets.exceptions.ConnectionClosedError:
        print('Disconnected from Minecraft')

async def start_server():
    print(f'Server starting, logging to {log_file_name}...')
    server = await websockets.serve(mineproxy, "localhost", 3000)
    print('Server started. On Minecraft, type /connect localhost:3000')
    await server.wait_closed()

asyncio.run(start_server())
