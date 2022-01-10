import os
from dotenv import load_dotenv
load_dotenv('../.env')

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 
URL = "retranslator-bot.herokuapp.com"
TEST_URL = "96b9-94-25-231-113.ngrok.io"
BOT_NAME = "martyn_retranslator_bot"
CHAT_ID = 129482161
