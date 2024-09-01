from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Accessing an environment variable
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
YOUR_APP_NAME = os.getenv('YOUR_APP_NAME')
if OPENROUTER_API_KEY is None:
    print("OPENROUTER_API_KEY is not set")
if YOUR_APP_NAME is None:
    print("YOUR_APP_NAME is not set")
