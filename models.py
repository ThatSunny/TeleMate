import google.generativeai as genai
import configparser

# Load Configurations
config = configparser.ConfigParser()
config.read('config.ini')
GEMINI_API_KEY = config.get('default', 'gemini_api_key')

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# List available models
models = list(genai.list_models())  # Convert generator to list

# Print all available models
print("Available models:", models)
