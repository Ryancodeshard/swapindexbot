"""
Swap index bot for NTU telegram users to swap their course indexes
@swapmyindexbot
"""
import os
from states import (
    start,
    myswaps,
    new,
    delete,
    findEntry,
    fallbacks
)

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

# Enable logging
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

token = os.environ["TOKEN"]

FIRST, SECOND, DELETING, NEWENTRY = range(4)


def lambda_handler(event,context):
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    initial_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start.start)],
        states={
            FIRST: [
                MessageHandler(Filters.regex('^(MySwaps)$'), myswaps.myswaps),
                MessageHandler(Filters.regex('^(NewSwap)$'), new.newswap),
            ],
            SECOND: [
                MessageHandler(Filters.regex('^(Delete)$'),
                               delete.deleteindex),
                MessageHandler(Filters.regex('^(Back)$'), start.start),
            ],
            DELETING: [MessageHandler(Filters.all, delete.deleting), ],
            NEWENTRY: [MessageHandler(Filters.all, new.newentry), ],
        },
        fallbacks=[CommandHandler("done", fallbacks.done),
                   CommandHandler("about", fallbacks.about)],
    )
    dispatcher.add_handler(initial_conv)
 
    updater.start_webhook(listen="0.0.0.0",
                      port=3978,
                      url_path=token)
    updater.bot.setWebhook(f'https://example.com/svc/{token}')
    return {
        'statusCode': 200
    }