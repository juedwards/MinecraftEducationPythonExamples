import asyncio
import websockets
import json
from uuid import uuid4

def process_message(json_message):
    # Check if json_message is already a Python dictionary
    if isinstance(json_message, dict):
        message = json_message
    else:
        try:
            # Attempt to convert the JSON string to a Python dictionary
            message = json.loads(json_message)
        except TypeError as e:
            print(f"Error processing message: {e}")
            return  # Exit the function if there's an error

    # Extract information from the message
    body = message.get('body', {})
    header = message.get('header', {})
    
    msg_text = body.get('message', '')
    sender = body.get('sender', '')
    event_name = header.get('eventName', '')
    
    # Act based on the message content
    if event_name == 'PlayerMessage':
        print(f"Received a message from {sender}: {msg_text}")
        # Here you can add more conditions to respond to different messages
        #if 'hello' in msg_text.lower():
            #print(f"Hello {sender}, how can I assist you?")
        # Add more conditions as needed

async def send_message(message):
    command = {
        "body": {
            "origin": {
                "type": "player"
            },
            "commandLine": f"/say {message}",
            "version": 1
        },
        "header": {
            "requestId": "0ffae098-00ff-ffff-abbbbbbbbbdf3344",
            "messagePurpose": "commandRequest",
            "version": 1,
            "messageType": "commandRequest"
        }
    }

    return command
            
# On Minecraft, when you type "/connect localhost:3000" it creates a connection
async def mineproxy(websocket, path):
    print('Connected')

    # Tell Minecraft to send all chat messages. Required once after Minecraft starts
    await websocket.send(
        json.dumps({
            "header": {
                "version": 1,                     # We're using the version 1 message protocol
                "requestId": str(uuid4()),        # A unique ID for the request
                "messageType": "commandRequest",  # This is a request ...
                "messagePurpose": "subscribe"     # ... to subscribe to ...
            },
            "body": {
                "eventName": "PlayerMessage"
            },
        }))

    try:
        # When MineCraft sends a message (e.g. on player chat), print it.
        async for msg in websocket:
            msg_dict = json.loads(msg)
            process_message(msg_dict)
            
            # Extract the message text
            msg_text = msg_dict.get('body', {}).get('message', '')

            # Check if the message is not a response to its own command to avoid infinite loop
            if not "Thanks for your message!" in msg_text:
                response_command = await send_message("Thanks for your message!")
                await websocket.send(json.dumps(response_command))

    except websockets.exceptions.ConnectionClosedError:
        print('Disconnected from MineCraft')


start_server = websockets.serve(mineproxy, host="localhost", port=3000)
print('Ready. On MineCraft, type /connect localhost:3000')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()