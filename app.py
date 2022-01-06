import logging
import os
import re

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from telebot.credentials import CHAT_ID, TOKEN, URL
from telebot.groups import groups
from utils import splitArr, fillKeyboard

logging.basicConfig(
    format='ℹ️  %(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

keyboard = fillKeyboard(groups)
reply_markup = InlineKeyboardMarkup(keyboard)

updater = Updater(TOKEN)
job_queue = updater.job_queue

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
        update.message.reply_text('Bark!')
        updater.bot.forwardMessage(
            chat_id=channel_id, from_chat_id=chat_id, message_id=message_id,
            disable_notification=True
        )

        return SEND

    if chat_id != CHAT_ID:
        
        return END

def post(update: Update, context: CallbackContext) -> None:
    message = update.message
    someta_channel_id = '-1001304984709' # test chat
    post_text=message.text.replace('POST', '')
    # scheduling_timeout = 7 * 24 * 60 * 60 # seconds of one week
    scheduling_timeout = 120
    
    job_queue.run_once(lambda x: updater.bot.send_message(
            chat_id=someta_channel_id,
            text=post_text, 
            disable_notification=True, 
            parse_mode="Markdown"
        ), scheduling_timeout
    )
     
    update.message.reply_text(
        "Woooooof"
    )
    
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
        entry_points=[CommandHandler('start', entry)],
        states={
            SEND: [
                CommandHandler('finish', done),
                CommandHandler('start', entry),
                MessageHandler(Filters.all, send),
            ],
            CHOICE: [
                CallbackQueryHandler(choice),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex(r'POST'), post),
            MessageHandler(Filters.all, done),
            CommandHandler('start', entry),
            CommandHandler('finish', done),
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
