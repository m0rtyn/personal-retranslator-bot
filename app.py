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
  message = update.message
  query = update.callback_query
  print("🚀 ~ file: app.py ~ line 35 ~ query", query)

  keyboard = [[
    InlineKeyboardButton("Чат Мартына", callback_data='@martynomicon'),
    InlineKeyboardButton("Kode Frontenders", callback_data='-'),
  ]]
  reply_markup = InlineKeyboardMarkup(keyboard)
  print("🚀 ~ file: app.py ~ line 28 ~ update.message", message)

  try:
    if message.chat.id == 129482161: ## id of personal chat with bot
      message.reply_text('Please choose:', reply_markup=reply_markup)

      if message.text:
        msg_id = message.message_id
        from_chat_id = message.chat.id
        # print("🚀 ~ file: app.py ~ line 42 ~ FROM_CHAT_ID", from_chat_id)

        bot.forwardMessage(chat_id=chat_id, from_chat_id=from_chat_id, message_id=msg_id)
  except AttributeError:
    print("EXCEPTION!", AttributeError)

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
