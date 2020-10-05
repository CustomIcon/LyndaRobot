# D A N K modules by @deletescape vvv
# based on
# https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata
import html
import random
import time
import requests
import re
import string
import asyncio
from io import BytesIO
import os
from pathlib import Path

from telegram import Update, ParseMode, Message
from telegram.ext import run_async, CallbackContext

import lynda.modules.fun_strings as fun_strings
from lynda import dispatcher
from lynda.modules.disable import DisableAbleCommandHandler
from lynda.modules.helper_funcs.chat_status import is_user_admin
from lynda.modules.helper_funcs.extraction import extract_user


@run_async
def slap(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text
    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == context.bot.id:
        temp = random.choice(fun_strings.SLAP_LYNDA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                context.bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    can_send_messages=False)
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:
        slapped_user = context.bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)
    else:
        user1 = context.bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    reply = temp.format(
        user1=user1,
        user2=user2,
        item=item,
        hits=hit,
        throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
def pat(update: Update, _):
    msg = update.effective_message
    pat = requests.get("https://some-random-api.ml/animu/pat").json()
    link = pat.get("link")
    if not link:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_video(link)


@run_async
def hug(update: Update, _):
    msg = update.effective_message
    hug = requests.get("https://some-random-api.ml/animu/hug").json()
    link = hug.get("link")
    if not link:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_video(link)


@run_async
def insult(update: Update, _):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(random.choice(fun_strings.INSULT_STRINGS))


@run_async
def shrug(update: Update, _):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(r"¯\_(ツ)_/¯")


@run_async
def table(update: Update, _):
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(fun_strings.TABLE))


__help__ = """
-> `/slap`
slap a user, or get slapped if not a reply.
-> `/shrug`
get shrug XD.
-> `/table`
get flip/unflip :v.
-> `/insult`
Insults the retar
-> `/pat`
pats a user by a reply to the message
-> `/hug`
hugs a user by a reply to the message
"""


PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
HUG_HANDLER = DisableAbleCommandHandler("hug", hug)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True)
SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug)
TABLE_HANDLER = DisableAbleCommandHandler("table", table)
INSULT_HANDLER = DisableAbleCommandHandler("insult", insult)

dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)
dispatcher.add_handler(INSULT_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(HUG_HANDLER)

__mod_name__ = "Fun"

__command_list__ = [
    "slap",
    "shrug",
    "table",
    "insult",
    "pat",
    "hug"]

__handlers__ = [
    SLAP_HANDLER,
    SHRUG_HANDLER,
    TABLE_HANDLER,
    INSULT_HANDLER,
    PAT_HANDLER,
    HUG_HANDLER]
