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
from haruka import dispatcher
from haruka.__main__ import STATS, USER_INFO
from haruka.modules.disable import DisableAbleCommandHandler
import wikipedia

def wiki(bot: Bot, update: Update, args):
    reply = " ".join(args)
    summary = '{} <a href="{}">more</a>'
    update.message.reply_text(summary.format(wikipedia.summary(reply, sentences=3), wikipedia.page(reply).url), pasrse_mode=HTML)
		
__help__ = """
 - /wiki text: Returns search from wikipedia for the input text
"""
__mod_name__ = "Wikipedia"
WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki, pass_args=True)
dispatcher.add_handler(WIKI_HANDLER)