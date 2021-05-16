from telegram import Update
from telegram.ext import CallbackContext
import requests
import os
token = os.environ["TOKEN"]
website = os.environ["website"]


def findEntry(update: Update, context: CallbackContext, courseCode, currentIndex, wantIndex, chatId, sendnoti):

    # duplicate search mode
    if int(chatId):
        response = requests.get(
            f"{website}swapindex/?courseCode={courseCode}&currentIndex={currentIndex}&wantIndex={wantIndex}&chatId={chatId}")
        if response.json():
            return True
        else:
            return False

    # swap search mode
    elif int(currentIndex):
        response = requests.get(
            f"{website}swapindex/?courseCode={courseCode}&currentIndex={currentIndex}&wantIndex={wantIndex}")
        if not response.json():
            # expand search to include those who are fine with any indexes
            response = requests.get(
                f"{website}swapindex/?courseCode={courseCode}&currentIndex={currentIndex}&wantIndex=0")
    else:
        response = requests.get(
            f"{website}swapindex/?courseCode={courseCode}&wantIndex={wantIndex}")

    if response.json():
        response_data = response.json()
        entry = response_data[0]

        other_username = entry["username"]
        chatId = entry["chatId"]
        text = f"Hi again @{other_username}! We have found a swap for you! Go to MySwaps to see it."
        if sendnoti:
            requests.get(
                f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatId}&text={text}")
            return True
        update.message.reply_text(
            "We found a possible swap for you\!Please contact the username listed under the username column to negotiate your swap\.", parse_mode='MarkdownV2')
        context.user_data["other_username"] = entry["username"]
        return True
    else:
        return False
