from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
FIRST, SECOND, DELETING, NEWENTRY = range(4)


def start(update: Update, context: CallbackContext) -> int:
    context.user_data["chat_id"] = update.message.chat.id
    context.user_data["username"] = update.message.from_user.username
    username = context.user_data["username"]
    start_keyboard = [['MySwaps', 'NewSwap']]
    update.message.reply_text(
        f"Hi @{username}\! *Welcome to SwapIndex bot\.*\n"
        "Click on MySwaps to see your current index/indices that you have posted "
        "or NewSwap to post a new index that you would like to swap\.\n"
        "Use /done anytime to exit the bot\.", parse_mode='MarkdownV2', reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True),
    )
    return FIRST
