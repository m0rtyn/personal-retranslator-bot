import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from telebot.credentials import CHAT_ID, TEST_URL, TOKEN, URL
from telebot.groups import groups

logging.basicConfig(
    format='ℹ️  %(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def splitArr(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

def fillKeyboard(dict):
    result = []
    for key, value in dict.items():
        result.append(InlineKeyboardButton(key, callback_data=value))

    return splitArr(result, 2)

keyboard = fillKeyboard(groups)
reply_markup = InlineKeyboardMarkup(keyboard)

updater = Updater(TOKEN)
CHOICE, SEND, DONE = range(3)

END = ConversationHandler.END

def entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

    return CHOICE


def choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    context.user_data['channel_id'] = query.data

    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")

    return SEND

def send(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    message = update.effective_message

    chat_id = message.chat.id
    message_id = message.message_id
    channel_id = user_data['channel_id']

    if chat_id == CHAT_ID: # id of personal chat with bot
        update.message.reply_text('Гав')
        updater.bot.forwardMessage(
            chat_id=channel_id, from_chat_id=chat_id, message_id=message_id,
            disable_notification=True
        )

        return SEND

    if chat_id != CHAT_ID:
        
        return END

def done(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"woof woof!"
    )

    context.user_data.clear()
    
    return END


def main() -> None:
    dispatcher = updater.dispatcher
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN
    )

    botUrl = 'https://{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN)
    updater.bot.set_webhook(botUrl)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('woof', entry)],
        states={
            CHOICE: [
                CallbackQueryHandler(choice),
            ],
            SEND: [
                CommandHandler('tyaf', done),
                CommandHandler('woof', entry),
                MessageHandler(Filters.all, send),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.all, done),
            CommandHandler('woof', entry),
            CommandHandler('tyaf', done),
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
