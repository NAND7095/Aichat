from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "6435225"
# -------------------------------------------------------------
API_HASH = "4e984ea35f854762dcde906dce426c2d"
# --------------------------------------------------------------
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING1 = getenv("STRING_SESSION", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", "7858950584"))
SUPPORT_GRP = "Nycreation_chatzone"
UPDATE_CHNL = "CreativeYdv"
OWNER_USERNAME = "Yo_Mysterious"
# config.py
OPENAI_API_KEY = "your_openai_api_key_here"
