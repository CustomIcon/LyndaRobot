from time import sleep
from typing import Optional, List
from telegram import TelegramError
from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import Filters, CommandHandler
from telegram.ext.dispatcher import run_async

import random
import lynda.modules.sql.users_sql as sql
from lynda.modules.helper_funcs.filters import CustomFilters
from lynda import dispatcher, OWNER_ID, LOGGER
from lynda.modules.disable import DisableAbleCommandHandler
USERS_GROUP = 4

MESSAGES = (
    "Happy birthday ",
    "Heppi burfdey ",
    "Hep burf ",
    "Happy day of birthing ",
    "Sadn't deathn't-day ",
    "Oof, you were born today ",
)


@run_async
def banall(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = str(args[0])
        all_mems = sql.get_chat_members(chat_id)
    else:
        chat_id = str(update.effective_chat.id)
        all_mems = sql.get_chat_members(chat_id)
    for mems in all_mems:
        try:
            bot.kick_chat_member(chat_id, mems.user)
            update.effective_message.reply_text(
                "Tried banning " + str(mems.user))
            sleep(0.1)
        except BadRequest as excp:
            update.effective_message.reply_text(
                excp.message + " " + str(mems.user))
            continue


@run_async
def snipe(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text(
            "Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of that group?")


@run_async
def birthday(bot: Bot, update: Update, args: List[str]):
    if args:
        username = str(",".join(args))
    # Bot typing before send messages
    bot.sendChatAction(update.effective_chat.id, "typing")
    for _ in range(5):
        bdaymessage = random.choice(MESSAGES)
        update.effective_message.reply_text(bdaymessage + username)


__help__ = """
*Owner only:*
- /banall: Ban all members from a chat
*Sudo only:*
- /snipe *chatid* *string*: Make me send a message to a specific chat.
*Admin only:*
- /birthday *@username*: Spam user with birthday wishes.
"""

__mod_name__ = "Special"

SNIPE_HANDLER = CommandHandler(
    "snipe",
    snipe,
    pass_args=True,
    filters=CustomFilters.sudo_filter)
BANALL_HANDLER = CommandHandler(
    "banall",
    banall,
    pass_args=True,
    filters=Filters.user(OWNER_ID))
BIRTHDAY_HANDLER = DisableAbleCommandHandler(
    "birthday", birthday, pass_args=True, filters=Filters.group)

dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(BANALL_HANDLER)
dispatcher.add_handler(BIRTHDAY_HANDLER)
