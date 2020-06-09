import html
import random
import time
from typing import List
import requests

from telegram import Bot, Update, ParseMode
from telegram.ext import run_async

import lynda.modules.fun_strings as fun_strings
from lynda import dispatcher
from lynda.modules.disable import DisableAbleCommandHandler
from lynda.modules.helper_funcs.chat_status import is_user_admin
from lynda.modules.helper_funcs.extraction import extract_user
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from lynda import dispatcher
from lynda.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
# D A N K modules by @deletescape vvv
# based on https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata
@run_async
def copypasta(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = random.choice(fun_strings.emojis)
    b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
    for c in message.reply_to_message.text:
        if c == " ":
            reply_text += random.choice(fun_strings.emojis)
        elif c in fun_strings.emojis:
            reply_text += c
            reply_text += random.choice(fun_strings.emojis)
        elif c.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(random.getrandbits(1)):
                reply_text += c.upper()
            else:
                reply_text += c.lower()
    reply_text += random.choice(fun_strings.emojis)
    message.reply_to_message.reply_text(reply_text)


@run_async
def bmoji(bot: Bot, update: Update):
    message = update.effective_message
    b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
    reply_text = message.reply_to_message.text.replace(b_char, "🅱️").replace(b_char.upper(), "🅱️")
    message.reply_to_message.reply_text(reply_text)


@run_async
def clapmoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "👏 "
    reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
    reply_text += " 👏"
    message.reply_to_message.reply_text(reply_text)
    
    
@run_async
def angrymoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "😡 "
    for i in message.reply_to_message.text:
        if i == " ":
            reply_text += " 😡 "
        else:
            reply_text += i
    reply_text += " 😡"
    message.reply_to_message.reply_text(reply_text)
    
    
@run_async
def crymoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "😭 "
    for i in message.reply_to_message.text:
        if i == " ":
            reply_text += " 😭 "
        else:
            reply_text += i
    reply_text += " 😭"
    message.reply_to_message.reply_text(reply_text)
    

@run_async
def me_too(bot: Bot, update: Update):
    message = update.effective_message
    if random.randint(0, 100) > 60:
        reply = random.choice(["Me too thanks", "Haha yes, me too", "Same lol", "Me irl"])
        message.reply_text(reply)  

@run_async
def weebify(bot: Bot, update: Update, args: List[str]):
    string = '  '.join(args).lower()
    for normiecharacter in string:
        if normiecharacter in fun_strings.NORMIEFONT:
            weebycharacter =  fun_strings.WEEBYFONT[fun_strings.NORMIEFONT.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)

    message = update.effective_message
    if message.reply_to_message:
        message.reply_to_message.reply_text(string)
    else:
        message.reply_text(string)

@run_async
def runs(bot: Bot, update: Update):
    update.effective_message.reply_text(random.choice(fun_strings.RUN_STRINGS))

@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_Kigyō_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(chat.id, message.from_user.id, until_date=mutetime, can_send_messages=False)
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)

@run_async
def pat(bot: Bot, update: Update):
    msg = update.effective_message
    pat = requests.get("https://some-random-api.ml/animu/pat").json()
    link = pat.get("link")
    if not link:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_video(link)

@run_async
def hug(bot: Bot, update: Update):
    msg = update.effective_message
    hug = requests.get("https://some-random-api.ml/animu/hug").json()
    link = hug.get("link")
    if not link:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_video(link)

@run_async
def roll(bot: Bot, update: Update):
    update.message.reply_text(random.choice(range(1, 7)))


@run_async
def toss(bot: Bot, update: Update):
    update.message.reply_text(random.choice(fun_strings.TOSS))


@run_async
def abuse(bot: Bot, update: Update):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(random.choice(fun_strings.ABUSE_STRINGS))

@run_async
def insult(bot: Bot, update: Update):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(random.choice(fun_strings.INSULT_STRINGS))


@run_async
def shrug(bot: Bot, update: Update):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(r"¯\_(ツ)_/¯")


@run_async
def bluetext(bot: Bot, update: Update):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text("/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS")


@run_async
def rlg(bot: Bot, update: Update):
    eyes = random.choice(fun_strings.EYES)
    mouth = random.choice(fun_strings.MOUTHS)
    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    update.message.reply_text(repl)


@run_async
def decide(bot: Bot, update: Update):
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(fun_strings.DECIDE))

@run_async
def table(bot: Bot, update: Update):
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(fun_strings.TABLE))

@run_async
def react(bot: Bot, update: Update):
    message = update.effective_message
    react = random.choice(fun_strings.REACTIONS)
    if message.reply_to_message:
        message.reply_to_message.reply_text(react)
    else:
        message.reply_text(react)

@run_async
def police(bot: Bot, update: Update):
    message = update.effective_message.reply_text('/police')
    for i in fun_strings.POLICE:
        message.edit_text(i)
        time.sleep(0.5)

@run_async
def moon(bot: Bot, update: Update):
    message = update.effective_message.reply_text('/moon')
    for i in fun_strings.MOON:
        message.edit_text(i)
        time.sleep(0.5)

@run_async
def clock(bot: Bot, update: Update):
    message = update.effective_message.reply_text('/moon')
    for i in fun_strings.CLOCK:
        message.edit_text(i)
        time.sleep(0.5)


__help__ = """
 - /runs: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /shrug : get shrug XD.
 - /table : get flip/unflip :v.
 - /decide : Randomly answers yes/no/maybe
 - /toss : Tosses A coin
 - /abuse : Abuses the cunt
 - /insult : Insults the retar
 - /bluetext : check urself :V
 - /roll : Roll a dice.
 - /rlg : Join ears,nose,mouth and create an emo ;-;
 - /pat : pats a user by a reply to the message
 - /hug : hugs a user by a reply to the message
 - /weebify <text>: returns a weebified text
 - /react: Reacts with a random reaction
 - Reply to a text with /🅱️ or /😂 or /👏
 - You can also use the text version of these : /bmoji or /copypasta or /clapmoji
 - /police : *Sirens* Polize iz here
 - /moon : Cycles all the phases of the moon emojis.
 - /clock : Cycles all the phases of the clock emojis.
"""

POLICE_HANDLER = DisableAbleCommandHandler(["police"], police)
MOON_HANDLER = DisableAbleCommandHandler(["moon"], moon)
CLOCK_HANDLER = DisableAbleCommandHandler(["clock"], clock)
REACT_HANDLER = DisableAbleCommandHandler("react", react)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
HUG_HANDLER = DisableAbleCommandHandler("hug", hug)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True)
ROLL_HANDLER = DisableAbleCommandHandler("roll", roll)
TOSS_HANDLER = DisableAbleCommandHandler("toss", toss)
SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug)
BLUETEXT_HANDLER = DisableAbleCommandHandler("bluetext", bluetext)
RLG_HANDLER = DisableAbleCommandHandler("rlg", rlg)
DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide)
TABLE_HANDLER = DisableAbleCommandHandler("table", table)
ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
INSULT_HANDLER = DisableAbleCommandHandler("insult", insult)
WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify, pass_args=True)
COPYPASTA_HANDLER = DisableAbleCommandHandler("copypasta", copypasta)
COPYPASTA_ALIAS_HANDLER = DisableAbleCommandHandler("😂", copypasta)
CLAPMOJI_HANDLER = DisableAbleCommandHandler("clapmoji", clapmoji)
CLAPMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("👏", clapmoji)
ANGRYMOJI_HANDLER = DisableAbleCommandHandler("angrymoji", angrymoji)
ANGRYMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("😡", angrymoji)
CRYMOJI_HANDLER = DisableAbleCommandHandler("crymoji", crymoji)
CRYMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("😭", crymoji)
BMOJI_HANDLER = DisableAbleCommandHandler("🅱️", bmoji)
BMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("bmoji", bmoji)

dispatcher.add_handler(POLICE_HANDLER)
dispatcher.add_handler(MOON_HANDLER)
dispatcher.add_handler(CLOCK_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(ROLL_HANDLER)
dispatcher.add_handler(TOSS_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(BLUETEXT_HANDLER)
dispatcher.add_handler(RLG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)
dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(INSULT_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(WEEBIFY_HANDLER)
dispatcher.add_handler(REACT_HANDLER)
dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(COPYPASTA_ALIAS_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(CLAPMOJI_ALIAS_HANDLER)
dispatcher.add_handler(ANGRYMOJI_HANDLER)
dispatcher.add_handler(ANGRYMOJI_ALIAS_HANDLER)
dispatcher.add_handler(CRYMOJI_HANDLER)
dispatcher.add_handler(CRYMOJI_ALIAS_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
dispatcher.add_handler(BMOJI_ALIAS_HANDLER)

__mod_name__ = "Fun"
__command_list__ = ["police", "moon", "clock", "runs", "slap", "roll", "toss", "shrug", "bluetext", "rlg", "decide", "table", "insult", "abuse", "pat", "hug", "weebify", "react", "copypasta", "😂", "clapmoji", "angrymoji", "😡", "crymoji", "😭", "🅱️", "bmoji"]
__handlers__ = [RUNS_HANDLER, SLAP_HANDLER, ROLL_HANDLER, TOSS_HANDLER, SHRUG_HANDLER, BLUETEXT_HANDLER, RLG_HANDLER,
                DECIDE_HANDLER, TABLE_HANDLER, ABUSE_HANDLER, INSULT_HANDLER, PAT_HANDLER, HUG_HANDLER, WEEBIFY_HANDLER,
                REACT_HANDLER, COPYPASTA_HANDLER, COPYPASTA_ALIAS_HANDLER, CLAPMOJI_HANDLER, CLAPMOJI_ALIAS_HANDLER,
                ANGRYMOJI_HANDLER, ANGRYMOJI_ALIAS_HANDLER, CRYMOJI_HANDLER, CRYMOJI_ALIAS_HANDLER, BMOJI_ALIAS_HANDLER,
                BMOJI_HANDLER, POLICE_HANDLER, MOON_HANDLER, CLOCK_HANDLER]
