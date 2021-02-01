#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Swap index bot for NTU telegram users
"""
import os
from dotenv import load_dotenv
load_dotenv()
token=os.getenv('swapindexbot_apitoken')

import logging, requests, json
from typing import Dict

from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

logswitch = True

FIRST, SECOND , DELETING, NEWENTRY = range(4)

#main menu
def start(update: Update, context: CallbackContext) -> int:
    if logswitch:
        logger.info("User @%s started bot", update.message.from_user.username)

    context.user_data["chat_id"] = update.message.chat.id
    context.user_data["username"] = update.message.from_user.username
    username = context.user_data["username"]
    start_keyboard = [['MySwaps','NewSwap']]

    update.message.reply_text(
        f"Hi @{username}\! *Welcome to SwapIndex bot\.*\n"
        "Click on MySwaps to see your current index/indices that you have posted "
        "or NewSwap to post a new index that you would like to swap\.\n"
        "Use /done anytime to exit the bot\.", parse_mode='MarkdownV2', reply_markup=ReplyKeyboardMarkup(start_keyboard,one_time_keyboard=True),
        )
    return FIRST


def myswaps(update: Update, context: CallbackContext) -> int:
    count = 1
    chatId = context.user_data["chat_id"]
    msg = "These are your current indexes you have listed\."
    msg+= "The bolded ones are indexes that the person in the Username column is willing to swap with you\.\n"
    msg += "No\.\|Course code\|Current Index\|Want Index\|Username\n"
    response = requests.get(f"http://127.0.0.1:8000/swapindex/?chatId={chatId}")
    if response.status_code == 200:
        responseData = response.json()
        if not responseData:
            msg+= "*Currently Empty*\n"
        for courses in responseData:
            courseCode = courses["courseCode"]
            currentIndex = courses["currentIndex"]
            wantIndexes = [courses["wantIndex"]]
            found = search(update,context,courseCode,wantIndexes,False)

            msg+=found*"*"
            msg += f"{count}\. {courseCode}\|{currentIndex}\|{wantIndexes[0]}\|"
            if found:
                other_username = context.user_data["other_username"]
                msg+= "@"+other_username
            else:
                msg+="No username"
            msg+=found*"*"
            msg+="\n"
            context.user_data[str(count)] = courses["id"]
            count+=1
            
    myswaps_keyboard = [['Delete','Back']]

    msg += "\nClick *Delete* to delete an entry or *Back* to go back to main menu\."
    update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup = ReplyKeyboardMarkup(myswaps_keyboard, one_time_keyboard=True),)
    return SECOND


def deleteindex(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Enter the number of the entry you would like to delete.",reply_markup=ReplyKeyboardRemove(),)
    return DELETING


def deleting(update: Update, context: CallbackContext) -> None:
    choice = update.message.text
    if choice.isdigit():
        try:
            delete_id = context.user_data[choice]
        except KeyError:
            update.message.reply_text("Choice is not within available range.")
        else:
            response = requests.delete(f"http://127.0.0.1:8000/swapindex/{delete_id}")
            if response.status_code == 204:
                update.message.reply_text(f"Entry number {choice} has been deleted.")
    else:
        update.message.reply_text("Thats not a number 0_o")
    return myswaps(update, context)


def newswap(update: Update, context: CallbackContext) -> int:
    newswap_keyboard = [['Back']]
    update.message.reply_text(
        "Enter your swap in the following format:\n"
        "CourseCode CurrentIndex WantIndex, where if there is more than one WantIndex, separate them with a space\n"
        "e.g.CZ1105 29380 29381 or\n"
        "CZ1105 29380 29381 29383 29384", reply_markup=ReplyKeyboardMarkup(newswap_keyboard,one_time_keyboard=True),
    )
    return NEWENTRY


def search(update: Update, context: CallbackContext, courseCode, wantIndexes, send_noti):
    response = requests.get(f"http://127.0.0.1:8000/swapindex/?courseCode={courseCode}")
    if response.status_code == 200:
        responseData = response.json()
    for courses in responseData:
        for wantIndex in wantIndexes:
            if int(wantIndex) == courses["currentIndex"]:
                other_username = courses["username"]
                if send_noti:
                    text = f"Hi again @{other_username}! We have found a swap for you! Go to MySwaps to see it."
                    chatId = courses["chatId"]
                    requests.get(f"https://api.telegram.org/bot1495647948:AAFVzdwVrslkryXo3YM3GPZXwj7Ds8n3WJI/sendMessage?chat_id={chatId}&text={text}")
                    update.message.reply_text("We found a possible swap for you! Go to MySwaps to see it.")
                context.user_data["other_username"] = courses["username"]
                return True
    return False


def newentry(update: Update, context: CallbackContext) -> int:
    payload_string = update.message.text
    if payload_string != "Back":
        username = context.user_data["username"]
        chatId = context.user_data["chat_id"]
        payload_string = payload_string.split()
        if payload_string[1] == payload_string[2]:
            update.message.reply_text("You can't want and have the same index 0_o")
            return start(update,context)
        context.user_data["courseCode"] = payload_string[0]
        try:
            context.user_data["wantIndexes"] = [payload_string[2]]
        except:
            update.message.reply_text("Wrong input format")
        else:
            if len(payload_string)>3:
                count = 0
                for i in range(2,len(payload_string)):
                    if i!=2:
                        context.user_data["wantIndexes"].append(payload_string[i])
                    payload = {
                        "courseCode":payload_string[0],
                        "currentIndex":payload_string[1],
                        "wantIndex":payload_string[i],
                        "username":username,
                        "chatId":chatId,
                    }
                    response = requests.post('http://127.0.0.1:8000/swapindex/', json=payload)
                    if response.status_code == 201:
                        count+=1
                        logger.info("Adding wantIndex %s",payload_string[i])
                update.message.reply_text(f"{count} entries have been added.")
            else:
                payload = {
                    "courseCode":payload_string[0],
                    "currentIndex":payload_string[1],
                    "wantIndex":payload_string[2],
                    "username":username,
                    "chatId":chatId,
                }
                response = requests.post('http://127.0.0.1:8000/swapindex/', json=payload)
            
                if response.status_code == 201:
                    update.message.reply_text("Entry has been added.")
            search(update,context,context.user_data["courseCode"],context.user_data["wantIndexes"],True)
    else:
        pass
    
    return start(update,context)


def done(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Bye! See you around next time...",reply_markup=ReplyKeyboardRemove(),)
    return ConversationHandler.END


def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("This bot was created by @ryantaw to help university students swap their indexes more easily.")


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    initial_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST: [
                MessageHandler(Filters.regex('^(MySwaps)$'), myswaps),
                MessageHandler(Filters.regex('^(NewSwap)$'), newswap),
            ],
            SECOND: [
                MessageHandler(Filters.regex('^(Delete)$'), deleteindex),
                MessageHandler(Filters.regex('^(Back)$'), start),
            ],
            DELETING: [MessageHandler(Filters.all, deleting),],
            NEWENTRY: [MessageHandler(Filters.all, newentry),],
        },
        fallbacks=[CommandHandler("done", done),CommandHandler("about", about)],
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
