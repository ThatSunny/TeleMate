from telethon import TelegramClient, events
import configparser

# Import your modules
from modules.user import start, save_contact
from modules.chat import handle_chat
from modules.file_analysis import analyze_file
from modules.web_search import web_search, fetch_results

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
    await start(event)  # Now, it works correctly

# 🟢 Handle phone number collection (Assuming it's done via contact sharing)
@client.on(events.NewMessage(func=lambda e: e.contact))
async def handle_contact(event):
    await save_contact(event)

# 🟢 Handle web search (/websearch command only)
@client.on(events.NewMessage(pattern="/websearch"))
async def handle_websearch(event):
    await web_search(event)

@client.on(events.NewMessage)  # This should only run fetch_results *after* /websearch
async def handle_websearch_query(event):
    if event.is_reply:  # Make sure it's a reply to the bot
        await fetch_results(event)

# 🟢 Handle AI Chat (default for normal messages)
@client.on(events.NewMessage)
async def handle_user_chat(event):
    if event.text.startswith("/"):  # Ignore unknown commands
        return
    await handle_chat(event)

# 🟢 Handle file uploads
@client.on(events.NewMessage(func=lambda e: e.document or e.photo))
async def handle_file_upload(event):
    await analyze_file(event)

print("✅ Bot is running...")
client.run_until_disconnected()
