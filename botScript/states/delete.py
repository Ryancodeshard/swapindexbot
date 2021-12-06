from .myswaps import myswaps
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext
import requests
import os
website = os.environ["WEBSITE"]
FIRST, SECOND, DELETING, NEWENTRY = range(4)


def deleteindex(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Enter the number of the entry you would like to delete.", reply_markup=ReplyKeyboardRemove(),)
    return DELETING


def deleting(update: Update, context: CallbackContext) -> None:
    choice = update.message.text
    chatId = context.user_data["chat_id"]
    if choice.isdigit():
        try:
            delete_id = context.user_data[choice]
        except KeyError:
            update.message.reply_text("Choice is not within available range.")
        else:
            response = requests.delete(
                f"{website}swapindex/{delete_id}")
            if response.status_code == 204:
                update.message.reply_text(
                    f"Entry number {choice} has been deleted.")
    else:
        update.message.reply_text("Thats not a number 0_o")
    return myswaps(update, context)
