import asyncio
import websockets
import json
import os
from uuid import uuid4
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Unique tag for identifying messages sent by the bot
BOT_TAG = "[AI]"

async def generate_gpt_response(message):
    prompt = f"Respond to the following message from a Minecraft player: {message}"
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    output = completion.choices[0].message.content.strip()
    print("Copilot says: " + output)

    # Split the output into lines and append the BOT_TAG to each line
    lines = output.split('\n')
    tagged_lines = [line + " " + BOT_TAG for line in lines[:5]]  # Limit to 5 lines
    return tagged_lines


async def process_message(json_message, websocket):
    if isinstance(json_message, dict):
        message = json_message
    else:
        try:
            message = json.loads(json_message)
        except TypeError as e:
            print(f"Error processing message: {e}")
            return

    body = message.get('body', {})
    header = message.get('header', {})
    
    msg_text = body.get('message', '')
    event_name = header.get('eventName', '')
    
    if event_name == 'PlayerMessage' and BOT_TAG not in msg_text:
        print(f"Received a message: {msg_text}")
        response_lines = await generate_gpt_response(msg_text)
        for line in response_lines:
            response_command = await send_message(line)
            await websocket.send(json.dumps(response_command))


async def send_message(message):
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
    return command

async def mineproxy(websocket, path):
    print('Connected')
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
        async for msg in websocket:
            await process_message(msg, websocket)
    except websockets.exceptions.ConnectionClosedError:
        print('Disconnected from Minecraft')

start_server = websockets.serve(mineproxy, "localhost", 3000)
print('Server started. On Minecraft, type /connect localhost:3000')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
