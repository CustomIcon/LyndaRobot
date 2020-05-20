import requests
import nekos
from PIL import Image
import os

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters

from tg_bot import dispatcher, updater
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.chat_status import is_user_admin, user_admin, sudo_plus

def neko(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'neko'
    msg.reply_photo(nekos.img(target))

def feet(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'feet'
    msg.reply_photo(nekos.img(target))

def yuri(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'yuri'
    msg.reply_photo(nekos.img(target))

def trap(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'trap'
    msg.reply_photo(nekos.img(target))

def futanari(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'futanari'
    msg.reply_photo(nekos.img(target))

def hololewd(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'hololewd'
    msg.reply_photo(nekos.img(target))

def lewdkemo(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'lewdkemo'
    msg.reply_photo(nekos.img(target))

def sologif(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'solog'
    msg.reply_video(nekos.img(target))

def feetgif(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'feetg'
    msg.reply_video(nekos.img(target))

def cumgif(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'cum'
    msg.reply_video(nekos.img(target))

def erokemo(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'erokemo'
    msg.reply_photo(nekos.img(target))

def lesbian(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'les'
    msg.reply_video(nekos.img(target))

def wallpaper(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'wallpaper'
    msg.reply_photo(nekos.img(target))

def lewdk(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'lewdk'
    msg.reply_photo(nekos.img(target))

def ngif(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'ngif'
    msg.reply_video(nekos.img(target))

def tickle(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'tickle'
    msg.reply_video(nekos.img(target))

def lewd(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'lewd'
    msg.reply_photo(nekos.img(target))

def feed(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'feed'
    msg.reply_video(nekos.img(target))

def eroyuri(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'eroyuri'
    msg.reply_photo(nekos.img(target))

def eron(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'eron'
    msg.reply_photo(nekos.img(target))

def cum(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'cum_jpg'
    msg.reply_photo(nekos.img(target))

def blowjobgif(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'bj'
    msg.reply_video(nekos.img(target))

def blowjob(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'blowjob'
    msg.reply_photo(nekos.img(target))

def nekonsfw(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'nsfw_neko_gif'
    msg.reply_video(nekos.img(target))

def solo(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'solo'
    msg.reply_photo(nekos.img(target))

def kemonomimi(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'kemonomimi'
    msg.reply_photo(nekos.img(target))

def avatarlewd(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'nsfw_avatar'
    with open("temp.png","wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp","webp")
    msg.reply_document(open("temp.webp","rb"))
    os.remove("temp.webp")

def gasm(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'gasm'
    with open("temp.png","wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp","webp")
    msg.reply_document(open("temp.webp","rb"))
    os.remove("temp.webp")

def poke(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'poke'
    msg.reply_video(nekos.img(target))

def anal(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'anal'
    msg.reply_video(nekos.img(target))

def hentai(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'hentai'
    msg.reply_photo(nekos.img(target))

def avatar(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'nsfw_avatar'
    with open("temp.png","wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp","webp")
    msg.reply_document(open("temp.webp","rb"))
    os.remove("temp.webp")

def erofeet(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'erofeet'
    msg.reply_photo(nekos.img(target))

def holo(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'holo'
    msg.reply_photo(nekos.img(target))

# def keta(bot: Bot, update: Update):
#     msg = update.effective_message
#     target = 'keta'
#     if not target:
#         msg.reply_text("No URL was received from the API!")
#         return
#     msg.reply_photo(nekos.img(target))

def pussygif(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'pussy'
    msg.reply_video(nekos.img(target))

def tits(bot: Bot, update: Update):
    msg = update.effective_message
    target = 'tits'
    msg.reply_photo(nekos.img(target))


def dva(bot: Bot, update: Update):
    msg = update.effective_message
    nsfw = requests.get("https://api.computerfreaker.cf/v1/dva").json()
    url = nsfw.get("url")
    # do shit with url if you want to
    if not url:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_photo(url)






__help__ = """
 - /hentai: Sends Random Hentai Images.
 - /neko: Sends Random neko source Images.
 - /dva: Sends Random D.VA source Images.
"""

__mod_name__ = "Nekos API"
HENTAI_HANDLER = DisableAbleCommandHandler("hentai", hentai)
NEKO_HANDLER = DisableAbleCommandHandler("neko", neko)
NEKONSFW_HANDLER = DisableAbleCommandHandler("nekonsfw", nekonsfw)
DVA_HANDLER = DisableAbleCommandHandler("dva", dva)


dispatcher.add_handler(HENTAI_HANDLER)
dispatcher.add_handler(NEKO_HANDLER)
dispatcher.add_handler(NEKONSFW_HANDLER)
dispatcher.add_handler(DVA_HANDLER)
# dispatcher.add_handler(YURI_HANDLER)
