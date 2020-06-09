import datetime
from typing import List
from random import randint
from tswift import Song

import requests
from telegram import Bot, Update, ParseMode
from telegram.ext import  CommandHandler, run_async

from lynda import dispatcher, TIME_API_KEY, CASH_API_KEY, WALL_API
from lynda.modules.disable import DisableAbleCommandHandler


def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(f"http://api.timezonedb.com/v2.1/list-time-zone"
                        f"?key={TIME_API_KEY}"
                        f"&format=json"
                        f"&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst").json()

    for zone in data["zones"]:
        for eachtype in findtype:
            if to_find in zone[eachtype].lower():
                country_name = zone['countryName']
                country_zone = zone['zoneName']
                country_code = zone['countryCode']

                if zone['dst'] == 1:
                    daylight_saving = "Yes"
                else:
                    daylight_saving = "No"

                date_fmt = r"%d-%m-%Y"
                time_fmt = r"%H:%M:%S"
                day_fmt = r"%A"
                gmt_offset = zone['gmtOffset']
                timestamp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=gmt_offset)
                current_date = timestamp.strftime(date_fmt)
                current_time = timestamp.strftime(time_fmt)
                current_day = timestamp.strftime(day_fmt)

                break

    try:
        result = (f"<b>Country :</b> <code>{country_name}</code>\n"
                  f"<b>Zone Name :</b> <code>{country_zone}</code>\n"
                  f"<b>Country Code :</b> <code>{country_code}</code>\n"
                  f"<b>Daylight saving :</b> <code>{daylight_saving}</code>\n"
                  f"<b>Day :</b> <code>{current_day}</code>\n"
                  f"<b>Current Time :</b> <code>{current_time}</code>\n"
                  f"<b>Current Date :</b> <code>{current_date}</code>")
    except:
        result = None

    return result


@run_async
def gettime(bot: Bot, update: Update):
    message = update.effective_message

    try:
        query = message.text.strip().split(" ", 1)[1]
    except:
        message.reply_text("Provide a country name/abbreviation/timezone to find.")
        return
    send_message = message.reply_text(f"Finding timezone info for <b>{query}</b>", parse_mode=ParseMode.HTML)

    query_timezone = query.lower()
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, ["countryCode"])
    else:
        result = generate_time(query_timezone, ["zoneName", "countryName"])

    if not result:
        send_message.edit_text(f"Timezone info not available for <b>{query}</b>", parse_mode=ParseMode.HTML)
        return

    send_message.edit_text(result, parse_mode=ParseMode.HTML)

@run_async
def convert(bot: Bot, update: Update):
    args = update.effective_message.text.split(" ", 3)
    if len(args) > 1:

        orig_cur_amount = float(args[1])

        try:
            orig_cur = args[2].upper()
        except IndexError:
            update.effective_message.reply_text("You forgot to mention the currency code.")
            return

        try:
            new_cur = args[3].upper()
        except IndexError:
            update.effective_message.reply_text("You forgot to mention the currency code to convert into.")
            return

        request_url = (f"https://www.alphavantage.co/query"
                       f"?function=CURRENCY_EXCHANGE_RATE"
                       f"&from_currency={orig_cur}"
                       f"&to_currency={new_cur}"
                       f"&apikey={CASH_API_KEY}")
        response = requests.get(request_url).json()
        try:
            current_rate = float(response['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        except KeyError:
            update.effective_message.reply_text(f"Currency Not Supported.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        update.effective_message.reply_text(f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}")
    else:
        update.effective_message.reply_text(__help__)

@run_async
def lyrics(bot: Bot, update: Update, args):
    msg = update.effective_message
    query = " ".join(args)
    song = ""
    if not query:
        msg.reply_text("You haven't specified which song to look for!")
        return
    else:
        song = Song.find_song(query)
        if song:
            if song.lyrics:
                reply = song.format()
            else:
                reply = "Couldn't find any lyrics for that song!"
        else:
            reply = "Song not found!"
        if len(reply) > 4090:
            with open("lyrics.txt", 'w') as f:
                f.write(f"{reply}\n\n\nOwO UwU OmO")
            with open("lyrics.txt", 'rb') as f:
                msg.reply_document(document=f,
                caption="Message length exceeded max limit! Sending as a text file.")
        else:
            msg.reply_text(reply)

@run_async
def wall(bot: Bot, update: Update, args):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    msg_id = update.effective_message.message_id
    query = " ".join(args)
    if not query:
        msg.reply_text("Please enter a query!")
        return
    else:
        caption = query
        term = query.replace(" ", "%20")
        json_rep = requests.get(f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}").json()
        if not json_rep.get("success"):
            msg.reply_text("An error occurred! Report this @LyndaEagleSupport")
        else:
            wallpapers = json_rep.get("wallpapers")
            if not wallpapers:
                msg.reply_text("No results found! Refine your search.")
                return
            else:
                index = randint(0, len(wallpapers)-1) # Choose random index
                wallpaper = wallpapers[index]
                wallpaper = wallpaper.get("url_image")
                wallpaper = wallpaper.replace("\\", "")
                bot.send_photo(chat_id, photo=wallpaper, caption='Preview',
                reply_to_message_id=msg_id, timeout=60)
                bot.send_document(chat_id, document=wallpaper,
                filename='wallpaper', caption=caption, reply_to_message_id=msg_id,
                timeout=60)

__help__ = """
**Get Time :**
Available queries : Country Code/Country Name/Timezone Name
 - /time <query> : Gives information about a timezone.

**Currency Converter: **
Example syntax: /cash 1 USD INR
 - /cash : currency converter

**Wallpapers: **
 - /wall <query>: get a a wallpaper from wall.alphacoders.com

**Lyrics: **
 - /lyrics <artist> <song>: returns the lyrics of that song.
"""

LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True)
WALL_HANDLER = DisableAbleCommandHandler("wall", wall, pass_args=True)
CONVERTER_HANDLER = CommandHandler('cash', convert)
TIME_HANDLER = DisableAbleCommandHandler("time", gettime)

dispatcher.add_handler(WALL_HANDLER)
dispatcher.add_handler(TIME_HANDLER)
dispatcher.add_handler(CONVERTER_HANDLER)
dispatcher.add_handler(LYRICS_HANDLER)

__mod_name__ = "Extras"
__command_list__ = ["time", "cash", "wall", "lyrics"]
__handlers__ = [TIME_HANDLER, CONVERTER_HANDLER, WALL_HANDLER, LYRICS_HANDLER]
