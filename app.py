import telegram
from flask import Flask, request

from telebot.credentials import URL, bot_token, bot_user_name, chat_id
from telebot.mastermind import get_response

global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
  # retrieve the message in JSON and then transform it to Telegram object
  update = telegram.Update.de_json(request.get_json(force=True), bot)

  msg_id = update.message.message_id
  from_chat_id = update.message.chat.id
  print("🚀 ~ file: app.py ~ line 22 ~ chat.id", update)

  if update.message.text:
    # print("UPDATE MESSAGE TEXT : ", update.message.text)
    # text = update.message.text.encode('utf-8').decode()
    # print("got text encoded message :", text)
    # response = get_response(text)
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
