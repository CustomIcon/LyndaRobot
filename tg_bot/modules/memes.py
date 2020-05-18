import random, re, string, io, asyncio
from PIL import Image
from io import BytesIO
import base64
from spongemock import spongemock
from zalgo_text import zalgo
import os
from pathlib import Path
import glob
import requests

import nltk # shitty lib, but it does work
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from typing import Optional, List
from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async
from deeppyer import deepfry

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

# D A N K modules by @deletescape vvv


@run_async
def owo(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        faces = ['(・`ω´・)',';;w;;','owo','UwU','>w<','^w^','\(^o\) (/o^)/','( ^ _ ^)∠☆','(ô_ô)','~:o',';____;', '(*^*)', '(>_', '(♥_♥)', '*(^O^)*', '((+_+))']
        reply_text = re.sub(r'[rl]', "w", message.reply_to_message.text)
        reply_text = re.sub(r'[ｒｌ]', "ｗ", message.reply_to_message.text)
        reply_text = re.sub(r'[RL]', 'W', reply_text)
        reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
        reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
        reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
        reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
        reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
        reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
        reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
        reply_text += ' ' + random.choice(faces)
        message.reply_to_message.reply_text(reply_text)


@run_async
def stretch(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message.reply_to_message.text)
        message.reply_to_message.reply_text(reply_text)


@run_async
def vapor(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    if not message.reply_to_message:
        if not args:
            message.reply_text("I need a message to convert to vaporwave text.")
        else:
            noreply = True
            data = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        noreply = False
        data = message.reply_to_message.text
    else:
        data = ''

    reply_text = str(data).translate(WIDE_MAP)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)



@run_async
def kan(bot: Bot, update: Update):
    msg = update.effective_message
    text = msg.reply_to_message
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}").json()
    url = r.get("message")
    if not url:
        msg.reply_text("No URL was received from the API!")
        return
    with open("temp.png","wb") as f:
        f.write(requests.get(url).content)
    img = Image.open("temp.png")
    img.save("temp.webp","webp")
    msg.reply_document(open("temp.webp","rb"))

@run_async
def changemymind(bot: Bot, update: Update):
    msg = update.effective_message
    text = msg.reply_to_message
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
    url = r.get("message")
    if not url:
        msg.reply_text("No URL was received from the API!")
        return
    with open("temp.png","wb") as f:
        f.write(requests.get(url).content)
    img = Image.open("temp.png")
    img.save("temp.webp","webp")
    msg.reply_document(open("temp.webp","rb"))

@run_async
def trumptweet(bot: Bot, update: Update):
    msg = update.effective_message
    text = msg.reply_to_message
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}").json()
    url = r.get("message")
    if not url:
        msg.reply_text("No URL was received from the API!")
        return
    with open("temp.png","wb") as f:
        f.write(requests.get(url).content)
    img = Image.open("temp.png")
    img.save("temp.webp","webp")
    msg.reply_document(open("temp.webp","rb"))


@run_async
def zalgotext(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = str('Insolant human, you must reply to something to zalgofy it!')

    reply_text = zalgo.zalgo().zalgofy(data)
    message.reply_text(reply_text)

# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv

@run_async
def forbesify(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = ''

    data = data.lower()
    accidentals = ['VB', 'VBD', 'VBG', 'VBN']
    reply_text = data.split()
    offset = 0

    # use NLTK to find out where verbs are
    tagged = dict(nltk.pos_tag(reply_text))

    # let's go through every word and check if it's a verb
    # if yes, insert ACCIDENTALLY and increase offset
    for k in range(len(reply_text)):
        i = reply_text[k + offset]
        if tagged.get(i) in accidentals:
            reply_text.insert(k + offset, 'accidentally')
            offset += 1

    reply_text = string.capwords(' '.join(reply_text))
    message.reply_to_message.reply_text(reply_text)


@run_async
def deepfryer(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.photo
        data2 = message.reply_to_message.sticker
    else:
        data = []
        data2 = []

    # check if message does contain media and cancel when not
    if not data and not data2:
        message.reply_text("What am I supposed to do with this?!")
        return

    # download last photo (highres) as byte array
    if data:
        photodata = data[len(data) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif data2:
        sticker = bot.get_file(data2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")

    # the following needs to be executed async (because dumb lib)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(process_deepfry(image, message.reply_to_message, bot))
    loop.close()


async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    image = await deepfry(
        img=image,
        token=os.getenv('DEEPFRY_TOKEN', ''),
        url_base='westeurope'
    )

    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')

    # send it back
    bio.seek(0)
    reply.reply_photo(bio)
    if Path("sticker.png").is_file():
        os.remove("sticker.png")

# shitty maymay modules made by @divadsn ^^^


@run_async
def shout(bot: Bot, update: Update, args):
    if len(args) == 0:
        update.effective_message.reply_text("Where is text?")
        return

    msg = "```"
    text = " ".join(args)
    result = []
    result.append(' '.join([s for s in text]))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


# no help string
__help__ = """
Some memes command, find it all out yourself!
- /owo: OWO de text
- /stretch: STRETCH de text
- /vapor: owo vapor dis
- /mock: mocks a spongebob image with text
- /shout: Write anything that u want it to should
- /zalgofy: reply to a message to g̫̞l̼̦i̎͡tͫ͢c̘ͭh̛̗ it out!
- /kan: reply a text to kannafy.
- /changemymind: reply a text to stickerize.
- /trumptweet: reply a text for trump tweet.
"""

__mod_name__ = "Memes and etc."

OWO_HANDLER = DisableAbleCommandHandler("owo", owo, admin_ok=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor", vapor, pass_args=True, admin_ok=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry", deepfryer, admin_ok=True)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)
KAN_HANDLER = DisableAbleCommandHandler("kan", kan)
CHANGEMYMIND_HANDLER = DisableAbleCommandHandler("changemymind", changemymind)
TRUMPTWEET_HANDLER = DisableAbleCommandHandler("trumptweet", trumptweet)

dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)
dispatcher.add_handler(KAN_HANDLER)
dispatcher.add_handler(CHANGEMYMIND_HANDLER)
dispatcher.add_handler(TRUMPTWEET_HANDLER)