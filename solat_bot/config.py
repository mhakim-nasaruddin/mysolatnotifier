# config.py
import os
from dotenv import load_dotenv # type: ignore

load_dotenv() # Load variables from .env file 

BOT_TOKEN = os.getenv("BOT_TOKEN")