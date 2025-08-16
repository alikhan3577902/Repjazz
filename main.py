
import time
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from flask import Flask, render_template_string
import os

# Telegram API setup
api_id = 21924891
api_hash = 'e36584063001075042be33ca7974d723'
bot_token = '8442972749:AAGunIF40qQhkMCY-LoqiACT2Ou_nyrsJQs'
channel_username = 'ZararEra'

# Telegram client start
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Flask setup
app = Flask(__name__)
logs = []

async def remove_all_members():
    try:
        channel = await client.get_entity(channel_username)

        participants = await client(GetParticipantsRequest(
            channel=channel,
            filter=ChannelParticipantsSearch(''),
            offset=0,
            limit=1000000,
            hash=0
        ))

        for member in participants.participants:
            if hasattr(member, 'admin_rights'):
                logs.append(f"Skipping {member.user_id} (Admin)")
                continue

            try:
                await client.kick_participant(channel, member.user_id)
                logs.append(f"Removed {member.user_id}")
                await asyncio.sleep(1)
            except Exception as e:
                logs.append(f"Failed {member.user_id}: {e}")

    except Exception as e:
        logs.append(f"Error: {e}")

@app.route("/")
def home():
    return render_template_string("""
        <h2>Telegram Member Removal Logs</h2>
        <pre>{{logs}}</pre>
    """, logs="\n".join(logs))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(remove_all_members())
    app.run(host="0.0.0.0", port=8080)
