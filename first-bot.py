import telegram
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from telebot.credentials import TOKEN, URL, bot_user_name, chat_id
from telebot.mastermind import get_response

global bot
global TOKEN

bot = telegram.Bot(token=TOKEN)
keyboard = [[
  InlineKeyboardButton("Чат Мартына", callback_data='@martynomicon'),
  InlineKeyboardButton("Kode Frontenders", callback_data='@kode_frontend')
]]
reply_markup = InlineKeyboardMarkup(keyboard)

app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
  response = request.get_json(force=True)
  update = Update.de_json(response, bot)


  if update.message:
    message = update.message

    if message.chat.id != 129482161: # id of personal chat with bot
      return 'ok'

      message.reply_text('Please choose:', reply_markup=reply_markup)
    try:

      if message.text:
        msg_id = message.message_id
        from_chat_id = message.chat.id
        # print("🚀 ~ file: app.py ~ line 42 ~ FROM_CHAT_ID", from_chat_id)

        bot.forwardMessage(chat_id=chat_id, from_chat_id=from_chat_id, message_id=msg_id)

    except Exception as e:
      if hasattr(e, 'message'):
          print(e.message)
      else:
          print(e)

  if update.callback_query:
    query = update.callback_query



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
