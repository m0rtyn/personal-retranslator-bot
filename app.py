import telegram
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telebot.credentials import URL, bot_token, bot_user_name, chat_id
from telebot.mastermind import get_response

global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
  response = request.get_json(force=True)
  update = Update.de_json(response, bot)

  keyboard = [[
    InlineKeyboardButton("Чат Мартына", callback_data='@martynomicon'),
    InlineKeyboardButton("Kode Frontenders", callback_data='-'),
  ]]
  reply_markup = InlineKeyboardMarkup(keyboard)

  update.message.reply_text('Please choose:', reply_markup=reply_markup)
  query = update.callback_query
  print("🚀 ~ file: app.py ~ line 35 ~ query", query)

  if update.message.text:
    msg_id = update.message.message_id
    from_chat_id = update.message.chat.id
    print("🚀 ~ file: app.py ~ line 22 ~ chat.id", update)

    bot.forwardMessage(chat_id=chat_id, from_chat_id=from_chat_id, message_id=msg_id)

  return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('https://{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
  app.run(threaded=True)
