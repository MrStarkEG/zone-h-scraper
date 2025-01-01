import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("ZONEH_USERNAME")
PASSWORD = os.getenv("ZONEH_PASSWORD")
ANTICAPTCHA_KEY = os.getenv("ANTICAPTCHA_KEY")
BASE_URL = "https://www.zone-h.org"
