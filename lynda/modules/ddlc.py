# import requests
# import os

# from telegram import Update, Bot, ParseMode
# from telegram.ext import run_async

# from lynda import dispatcher
# from lynda.modules.disable import DisableAbleCommandHandler

# @run_async
# def ddlc(bot: Bot, update: Update):
#     msg = update.effective_message
#     args = update.effective_message.text.split(" ", 5)
#     character = args[1]
#     background = args[2]
#     body = args[3]
#     face = args[4]
#     text = args[5]
#     rq = requests.get(f"https://nekobot.xyz/api/imagegen?type=ddlc&character={character}&background={background}&body={body}&face={face}&text={text}").json()
#     message = rq.get("message")
#     # do shit with url if you want to
#     if not message:
#         msg.reply_text("No URL was received from the API!")
#         return
#     msg.reply_photo(message)


# __help__ = """[Documentation](https://telegra.ph/DDLC-Documentation-05-18)"""
# __mod_name__ = "DDLC"

# DDLC_HANDLER = DisableAbleCommandHandler("ddlc", ddlc)

# dispatcher.add_handler(DDLC_HANDLER)

