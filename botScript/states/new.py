from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
import requests
import os

from .findEntry import findEntry
from .myswaps import myswaps
website = os.environ["WEBSITE"]

FIRST, SECOND, DELETING, NEWENTRY = range(4)


def newswap(update: Update, context: CallbackContext) -> int:
    newswap_keyboard = [['Back']]
    text = ("Enter your swap in the following space separated format:\n"
            "*CourseCode CurrentIndex WantIndex*\n"
            "e\.g\.\n"
            "any index except my current one:\n"
            "*CZ1105 29380 0*\n"
            "1 want index:\n"
            "*CZ1105 29380 29381* \n"
            "3 want indexes:\n"
            "*CZ1105 29380 29381 29383 29384*")
    update.message.reply_text(text, parse_mode='MarkdownV2', reply_markup=ReplyKeyboardMarkup(
        newswap_keyboard, one_time_keyboard=True))
    return NEWENTRY


def newentry(update: Update, context: CallbackContext) -> None:
    # need to do data validation
    payload_string = update.message.text
    if payload_string != "Back":
        username = context.user_data["username"]
        chatId = context.user_data["chat_id"]
        payload_string = payload_string.split()
        courseCode = payload_string[0]  # validate
        currentIndex = payload_string[1]
        wantIndexes = payload_string[2:]
        if currentIndex in wantIndexes:
            update.message.reply_text(
                "You can't want and have the same index 0_o")
            return newswap(update, context)

        count = 0
        if '0' in wantIndexes:
            wantIndexes = ['0']
        for wantIndex in wantIndexes:
            if findEntry(Update, context, courseCode, currentIndex, wantIndex, chatId, 0):
                continue  # duplicate found

            payload = {
                "courseCode": courseCode,
                "currentIndex": currentIndex,
                "wantIndex": wantIndex,
                "username": username,
                "chatId": chatId,
            }
            response = requests.post(
                f"{website}swapindex/", json=payload)

            if response.status_code == 201:
                findEntry(update, context, courseCode,
                          wantIndex, currentIndex, 0, 1)
                count += 1
        update.message.reply_text(f"{count} entries have been added.")

    return myswaps(update, context)
