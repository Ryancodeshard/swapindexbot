#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Swap index bot for NTU telegram users to swap their course indexes
@swapmyindexbot
"""
from dotenv import dotenv_values
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

token = dotenv_values('.env')["TOKEN"]

FIRST, SECOND, DELETING, NEWENTRY = range(4)


def main() -> None:
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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
