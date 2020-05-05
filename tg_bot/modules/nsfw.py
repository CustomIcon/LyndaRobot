from telegram import ChatAction
import html
import urllib.request
import re
import json
from typing import Optional, List
import time
import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus, urlencode
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.chat_status import is_user_admin, user_admin

def butts(bot: Bot, update: Update):
    nsfw = requests.get('http://api.obutts.ru/noise/1').json()[0]["preview"]
    final = "http://media.obutts.ru/{}".format(nsfw)
    update.message.reply_photo(final)

def boobs(bot: Bot, update: Update):
    nsfw = requests.get('http://api.oboobs.ru/noise/1').json()[0]["preview"]
    final = "http://media.oboobs.ru/{}".format(nsfw)
    update.message.reply_photo(final)

def hentai(bot: Bot, update: Update):
    message = update.effective_message
    nsfw = requests.get('https://api.computerfreaker.cf/v1/hentai').json
    if not shibe:
        await update.effective_message.reply_text("`Couldn't fetch a cat for you :(`")
        return
    try:
        update.effective_message(file=json[0], reply_to=message.reply_photo)

__help__ = """
 - /boobs: Sends Random tiddie pic.
 - /butts: Sends Random bun pic.
 - /hentai: Sends Random Hentai Images.
"""

__mod_name__ = "NSFW"
BUTTS_HANDLER = DisableAbleCommandHandler("butts", butts)
BOOBS_HANDLER = DisableAbleCommandHandler("boobs", boobs)
HENTAI_HANDLER = DisableAbleCommandHandler("hentai", hentai)

dispatcher.add_handler(BUTTS_HANDLER)
dispatcher.add_handler(BOOBS_HANDLER)
dispatcher.add_handler(HENTAI_HANDLER)
