from telethon import TelegramClient, events
import configparser

# Import modules
from modules.user import start, save_contact
from modules.chat import handle_chat
from modules.file_analysis import analyze_file
from modules.web_search import fetch_results

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('default', 'api_id')
API_HASH = config.get('default', 'api_hash')
BOT_TOKEN = config.get('default', 'bot_token')

# Start Telegram Client
client = TelegramClient("sessions/Bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🟢 Handle /start command
@client.on(events.NewMessage(pattern="/start"))
async def handle_start(event):
    await start(event)

# 🟢 Handle contact sharing
@client.on(events.NewMessage(func=lambda e: e.contact))
async def handle_contact(event):
    await save_contact(event)

# 🟢 Handle web searches
@client.on(events.NewMessage(pattern=r"/websearch (.+)"))
async def handle_websearch(event):
    query = event.pattern_match.group(1)
    await fetch_results(event, query)

# 🟢 Handle file uploads
@client.on(events.NewMessage(func=lambda e: e.document or e.photo))
async def handle_file_upload(event):
    await analyze_file(event)

# 🟢 Handle AI chat for regular messages
@client.on(events.NewMessage)
async def handle_user_chat(event):
    if event.text.startswith("/") or event.document or event.photo:
        return  # Ignore commands and files
    await handle_chat(event)

print("✅ Bot is running...", flush=True)
client.run_until_disconnected()