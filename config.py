import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")