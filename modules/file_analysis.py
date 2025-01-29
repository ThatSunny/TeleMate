import google.generativeai as genai
from modules.database import files_collection
from telethon import events
import configparser
from datetime import datetime
from PIL import Image
from io import BytesIO

# Load Configurations
config = configparser.ConfigParser()
config.read('config.ini')
GEMINI_API_KEY = config.get('default', 'gemini_api_key')

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

async def analyze_file(event):
    chat_id = event.chat_id
    file_name = event.message.file.name if event.message.document else "image.jpg"

    # Download the file
    file_path = await event.message.download_media()

    # Read the file content as bytes
    with open(file_path, "rb") as f:
        file_content = f.read()

    try:
        # Convert the byte content to a PIL Image (optional step, in case we want to inspect the image)
        image = Image.open(BytesIO(file_content))

        # Pass the byte content of the image to the Gemini AI model (using gemini-1.5-flash-latest)
        response = genai.GenerativeModel("models/gemini-1.5-flash-latest").generate_content([file_content])

        # Store file metadata in MongoDB
        files_collection.insert_one({
            "chat_id": chat_id,
            "filename": file_name,
            "description": response.text,
            "timestamp": datetime.now()
        })

        # Send the analysis result back to the user
        await event.respond(f"🖼️ File Analysis:\n{response.text}")
    
    except Exception as e:
        # Handle the case where the file is not a valid image or an error occurs during analysis
        print(f"Error processing image: {e}")
        await event.respond("Oops! Something went wrong with the image upload. Please try again.")
