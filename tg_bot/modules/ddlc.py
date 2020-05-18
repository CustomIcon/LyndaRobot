import requests
import os

from telegram import Update, Bot
from telegram.ext import run_async

from tg_bot import dispatcher, updater
from tg_bot.modules.disable import DisableAbleCommandHandler

def ddlc(bot: Bot, update: Update):
    msg = update.effective_message
    character = msg.text.split(' ', 1)
    background = msg.text.split(' ', 2)
    body = msg.text.split(' ', 3)
    face = msg.text.split(' ', 4)
    text = msg.text.split(' ', 5)
    rq = requests.get(f"https://nekobot.xyz/api/imagegen?type=ddlc&character={character}&background={background}&body={body}&face={face}&text={text}").json()
    message = rq.get("message")
    # do shit with url if you want to
    if not message:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_photo(message)


__help__ = """
 - /ddlc - generates a poster inspired by Doki Doki Literature Club
   Usage: /ddlc <character> <background> <body> <face> <text>
   Characters: monika, yuri, natsuki, sayori (m, y, n , s)
   Background: bedroom, class, closet, club, corridor, house, kitchen, residential, sayori_bedroom
   Body: there is only 1 or 2 for monika and 1, 1b, 2, 2b for the rest
   Face: Every Alphabet Letter, For Yuri (y1, y2, y3, y4, y5, y6, y7)
   Text = BOTTOM TEXT
"""
__mod_name__ = "DDLC"

DDLC_HANDLER = DisableAbleCommandHandler("ddlc", ddlc)

dispatcher.add_handler(DDLC_HANDLER)

