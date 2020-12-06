import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Filters, MessageHandler, Updater)

from telebot.credentials import TOKEN, URL, bot_user_name, chat_id

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[
        InlineKeyboardButton("Чат Мартына", callback_data='@martynomicon'),
        InlineKeyboardButton("Kode Frontenders", callback_data='@kode_frontend')
    ]]


    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
  query = update.callback_query

  # CallbackQueries need to be answered, even if no notification to the user is needed
  query.answer()

  query.edit_message_text(text=f"Selected option: {query.data}")
  print("🚀 ~ file: app.py ~ line 41 ~ update.message", update.message)

  if update.message:
    message = update.message

    if message.chat.id != 129482161: # id of personal chat with bot
      return 'ok'
    
    if message.text:
      msg_id = message.message_id
      from_chat_id = query.data

      updater.bot.forwardMessage(chat_id=chat_id, from_chat_id=from_chat_id, message_id=msg_id)

def main():
  updater = Updater(TOKEN)
  updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TOKEN)

  botUrl = 'https://{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN)
  updater.bot.set_webhook(botUrl)

  updater.dispatcher.add_handler(CommandHandler('start', start))
  updater.dispatcher.add_handler(CallbackQueryHandler(button))

  # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT
  updater.idle()

if __name__ == '__main__':
    main()
