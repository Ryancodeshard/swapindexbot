from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
import requests
from .findEntry import findEntry

from dotenv import dotenv_values
website = dotenv_values('.env')["website"]


FIRST, SECOND, DELETING, NEWENTRY = range(4)


def myswaps(update: Update, context: CallbackContext) -> int:
    count = 1
    chatId = context.user_data["chat_id"]
    msg = "These are your current swaps you have listed\.0 indicates all indexes\."
    msg += "The *bolded* ones are indexes that the person in the Username column is willing to swap with you\.\n"
    msg += "No\.\|Course code\|Current Index\|Want Index\|Username\n"
    response = requests.get(
        f"{website}swapindex/?chatId={chatId}")
    if response.status_code == 200:
        responseData = response.json()
        if not responseData:
            msg += "*Currently Empty*\n"
        for entry in responseData:
            courseCode = entry["courseCode"]
            currentIndex = entry["currentIndex"]
            wantIndex = entry["wantIndex"]

            if findEntry(update, context, courseCode, wantIndex, currentIndex, 0, 0):
                msg += f"*{count}\. {courseCode}\|{currentIndex}\|{wantIndex}\|"
                msg += "@"+context.user_data["other_username"]+"*"
            else:
                msg += f"{count}\. {courseCode}\|{currentIndex}\|{wantIndex}\|"
                msg += "no match yet"
            msg += "\n"
            context.user_data[str(count)] = entry["entryId"]
            count += 1

    myswaps_keyboard = [['Delete', 'Back']]

    msg += "\nClick *Delete* to delete an entry or *Back* to go back to main menu\."
    update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=ReplyKeyboardMarkup(
        myswaps_keyboard, one_time_keyboard=True),)
    return SECOND
