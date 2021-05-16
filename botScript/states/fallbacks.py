from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler


def done(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Bye! See you around next time...", reply_markup=ReplyKeyboardRemove(),)
    return ConversationHandler.END


def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "This bot was created to help university students swap their indexes more easily :) Check out the repo: https://github.com/Ryancodeshard/swapindexbot")
