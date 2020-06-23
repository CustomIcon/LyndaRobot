import datetime
from random import randint
from gtts import gTTS
import os
import re
import urllib
from datetime import datetime
import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import requests
from typing import Optional, List
from telegram import ParseMode, InputMediaPhoto, Update, Bot, TelegramError, ChatAction
from telegram.ext import CommandHandler, run_async
from lynda import dispatcher, TIME_API_KEY, CASH_API_KEY, WALL_API
from lynda.modules.disable import DisableAbleCommandHandler

opener = urllib.request.build_opener()
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.38 Safari/537.36'
#useragent = 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]


@run_async
def app(bot: Bot, update: Update):
    message = update.effective_message
    try:
        progress_message = update.effective_message.reply_text(
            "Searching.... ")
        app_name = message.text[len('/app '):]
        remove_space = app_name.split(' ')
        final_name = '+'.join(remove_space)
        page = requests.get(
            f"https://play.google.com/store/search?q={final_name}&c=apps")
        soup = BeautifulSoup(page.content, 'lxml', from_encoding='utf-8')
        results = soup.findAll("div", "ZmHEEd")
        app_name = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'WsMG1c nnK0zc').text
        app_dev = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'KoLSrc').text
        app_dev_link = "https://play.google.com" + results[0].findNext(
            'div', 'Vpfmgd').findNext('a', 'mnKHRc')['href']
        app_rating = results[0].findNext('div', 'Vpfmgd').findNext(
            'div', 'pf5lIe').find('div')['aria-label']
        app_link = "https://play.google.com" + results[0].findNext(
            'div', 'Vpfmgd').findNext('div', 'vU6FJ p63iDd').a['href']
        app_icon = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'uzcko').img['data-src']
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += "\n\n<code>Developer :</code> <a href='" + app_dev_link + "'>"
        app_details += app_dev + "</a>"
        app_details += "\n<code>Rating :</code> " + app_rating.replace(
            "Rated ", "⭐️ ").replace(" out of ", "/").replace(
                " stars", "", 1).replace(" stars", "⭐️").replace("five", "5")
        app_details += "\n<code>Features :</code> <a href='" + \
            app_link + "'>View in Play Store</a>"
        message.reply_text(
            app_details,
            disable_web_page_preview=False,
            parse_mode='html')
    except IndexError:
        message.reply_text(
            "No result found in search. Please enter **Valid app name**")
    except Exception as err:
        message.reply_text(err)
    progress_message.delete()


@run_async
def ud(bot: Bot, update: Update):
    message = update.effective_message
    text = message.text[len('/ud '):]
    results = requests.get(
        f'http://api.urbandictionary.com/v0/define?term={text}').json()
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_\n\n_{results["list"][0]["author"]}_'
    except Exception:
        reply_text = "No results found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


@run_async
def tts(bot: Bot, update: Update, args):
    datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    datetime.now().strftime("%d%m%y-%H%M%S%f")
    reply = " ".join(args)
    update.message.chat.send_action(ChatAction.RECORD_AUDIO)
    lang = "ml"
    tts = gTTS(reply, lang)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        lang = "en"
        tts = gTTS(reply, lang)
        tts.save("k.mp3")
    with open("k.mp3", "rb") as speech:
        update.message.reply_voice(speech, quote=False)


@run_async
def reverse(bot: Bot, update: Update, args: List[str]):
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    msg = update.effective_message
    chat_id = update.effective_chat.id
    rtmid = msg.message_id
    imagename = "okgoogle.png"

    reply = msg.reply_to_message
    if reply:
        if reply.sticker:
            file_id = reply.sticker.file_id
        elif reply.photo:
            file_id = reply.photo[-1].file_id
        elif reply.document:
            file_id = reply.document.file_id
        else:
            msg.reply_text("Reply to an image or sticker to lookup.")
            return
        image_file = bot.get_file(file_id)
        image_file.download(imagename)
        if args:
            txt = args[0]
            try:
                lim = int(txt)
            except Exception:
                lim = 2
        else:
            lim = 2
    elif args and not reply:
        splatargs = msg.text.split(" ")
        if len(splatargs) == 3:
            img_link = splatargs[1]
            try:
                lim = int(splatargs[2])
            except Exception:
                lim = 2
        elif len(splatargs) == 2:
            img_link = splatargs[1]
            lim = 2
        else:
            msg.reply_text("/reverse <link> <amount of images to return.>")
            return
        try:
            urllib.request.urlretrieve(img_link, imagename)
        except HTTPError as HE:
            if HE.reason == 'Not Found':
                msg.reply_text("Image not found.")
                return
            elif HE.reason == 'Forbidden':
                msg.reply_text(
                    "Couldn't access the provided link, The website might have blocked accessing to the website by bot or the website does not existed.")
                return
        except URLError as UE:
            msg.reply_text(f"{UE.reason}")
            return
        except ValueError as VE:
            msg.reply_text(
                f"{VE}\nPlease try again using http or https protocol.")
            return
    else:
        msg.reply_markdown(
            "Please reply to a sticker, or an image to search it!\nDo you know that you can search an image with a link too? `/reverse [picturelink] <amount>`.")
        return

    try:
        searchUrl = 'https://www.google.com/searchbyimage/upload'
        multipart = {
            'encoded_image': (
                imagename,
                open(
                    imagename,
                    'rb')),
            'image_content': ''}
        response = requests.post(
            searchUrl,
            files=multipart,
            allow_redirects=False)
        fetchUrl = response.headers['Location']

        if response != 400:
            xx = bot.send_message(
                chat_id, "Image was successfully uploaded to Google."
                "\nParsing source now. Maybe.", reply_to_message_id=rtmid)
        else:
            xx = bot.send_message(
                chat_id,
                "Google told me to go away.",
                reply_to_message_id=rtmid)
            return

        os.remove(imagename)
        match = ParseSauce(fetchUrl + "&hl=en")
        guess = match['best_guess']
        if match['override'] and match['override'] != '':
            imgspage = match['override']
        else:
            imgspage = match['similar_images']

        if guess and imgspage:
            xx.edit_text(
                f"[{guess}]({fetchUrl})\nLooking for images...",
                parse_mode='Markdown',
                disable_web_page_preview=True)
        else:
            xx.edit_text("Couldn't find anything.")
            return

        images = scam(imgspage, lim)
        if len(images) == 0:
            xx.edit_text(
                f"[{guess}]({fetchUrl})\n[Visually similar images]({imgspage})"
                "\nCouldn't fetch any images.",
                parse_mode='Markdown',
                disable_web_page_preview=True)
            return

        imglinks = []
        for link in images:
            lmao = InputMediaPhoto(media=str(link))
            imglinks.append(lmao)

        bot.send_media_group(
            chat_id=chat_id,
            media=imglinks,
            reply_to_message_id=rtmid)
        xx.edit_text(
            f"[{guess}]({fetchUrl})\n[Visually similar images]({imgspage})",
            parse_mode='Markdown',
            disable_web_page_preview=True)
    except TelegramError as e:
        print(e)
    except Exception as exception:
        print(exception)


def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, 'html.parser')

    results = {
        'similar_images': '',
        'override': '',
        'best_guess': ''
    }

    try:
        for bess in soup.findAll('a', {'class': 'PBorbe'}):
            url = 'https://www.google.com' + bess.get('href')
            results['override'] = url
    except Exception:
        pass

    for similar_image in soup.findAll('input', {'class': 'gLFyf'}):
        url = 'https://www.google.com/search?tbm=isch&q=' + \
            urllib.parse.quote_plus(similar_image.get('value'))
        results['similar_images'] = url

    for best_guess in soup.findAll('div', attrs={'class': 'r5a77d'}):
        results['best_guess'] = best_guess.get_text()

    return results


def scam(imgspage, lim):
    """Parse/Scrape the HTML code for the info we want."""

    single = opener.open(imgspage).read()
    decoded = single.decode('utf-8')
    if int(lim) > 10:
        lim = 10

    imglinks = []
    counter = 0

    pattern = r'^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$'
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        imglinks.append(imglink)
        if counter >= int(lim):
            break

    return imglinks


def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(
        f"http://api.timezonedb.com/v2.1/list-time-zone"
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
                timestamp = datetime.datetime.now(
                    datetime.timezone.utc) + datetime.timedelta(seconds=gmt_offset)
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
    except Exception:
        result = None

    return result


@run_async
def gettime(bot: Bot, update: Update):
    message = update.effective_message

    try:
        query = message.text.strip().split(" ", 1)[1]
    except Exception:
        message.reply_text(
            "Provide a country name/abbreviation/timezone to find.")
        return
    send_message = message.reply_text(
        f"Finding timezone info for <b>{query}</b>",
        parse_mode=ParseMode.HTML)

    query_timezone = query.lower()
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, ["countryCode"])
    else:
        result = generate_time(query_timezone, ["zoneName", "countryName"])

    if not result:
        send_message.edit_text(
            f"Timezone info not available for <b>{query}</b>",
            parse_mode=ParseMode.HTML)
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
            update.effective_message.reply_text(
                "You forgot to mention the currency code.")
            return

        try:
            new_cur = args[3].upper()
        except IndexError:
            update.effective_message.reply_text(
                "You forgot to mention the currency code to convert into.")
            return

        request_url = (f"https://www.alphavantage.co/query"
                       f"?function=CURRENCY_EXCHANGE_RATE"
                       f"&from_currency={orig_cur}"
                       f"&to_currency={new_cur}"
                       f"&apikey={CASH_API_KEY}")
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        except KeyError:
            update.effective_message.reply_text("Currency Not Supported.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        update.effective_message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}")
    else:
        update.effective_message.reply_text(__help__)


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
        json_rep = requests.get(
            f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}").json()
        if not json_rep.get("success"):
            msg.reply_text("An error occurred! Report this @LyndaEagleSupport")
        else:
            wallpapers = json_rep.get("wallpapers")
            if not wallpapers:
                msg.reply_text("No results found! Refine your search.")
                return
            else:
                index = randint(0, len(wallpapers) - 1)  # Choose random index
                wallpaper = wallpapers[index]
                wallpaper = wallpaper.get("url_image")
                wallpaper = wallpaper.replace("\\", "")
                bot.send_photo(chat_id, photo=wallpaper, caption='Preview',
                               reply_to_message_id=msg_id, timeout=60)
                bot.send_document(
                    chat_id,
                    document=wallpaper,
                    filename='wallpaper',
                    caption=caption,
                    reply_to_message_id=msg_id,
                    timeout=60)


@run_async
def covid(bot: Bot, update: Update):
    message = update.effective_message
    text = message.text.split(' ', 1)
    if len(text) == 1:
        r = requests.get("https://corona.lmao.ninja/v2/all").json()
        reply_text = f"**Global Totals** 🦠\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    else:
        variabla = text[1]
        r = requests.get(
            f"https://corona.lmao.ninja/v2/countries/{variabla}").json()
        reply_text = f"**Cases for {r['country']} 🦠**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


__help__ = """
**Covid - 19:
 - /covid To get Global data
 - /covid <country> To get data of a country

**Urban Dictionary :**
 - /ud <word>: Type the word or expression you want to search use.

**Get Time :**
Available queries : Country Code/Country Name/Timezone Name
 - /time <query> : Gives information about a timezone.

**Currency Converter: **
Example syntax: /cash 1 USD INR
 - /cash : currency converter

**Wallpapers: **
 - /wall <query>: get a wallpaper from wall.alphacoders.com

**Google Reverse Search: **
 - /reverse: Does a reverse image search of the media which it was replied to.

**Text-to-Speach**
 - /tts <sentence>:  Text to Speech!

**Last FM:**
 - /setuser <username>: sets your last.fm username.
 - /clearuser: removes your last.fm username from the bot's database.
 - /lastfm: returns what you're scrobbling on last.fm.

**Playstore:**
 - /app <app name>: finds an app in playstore for you
"""
APP_HANDLER = DisableAbleCommandHandler("app", app)
UD_HANDLER = DisableAbleCommandHandler("ud", ud)
COVID_HANDLER = DisableAbleCommandHandler(["covid", "corona"], covid)
WALL_HANDLER = DisableAbleCommandHandler("wall", wall, pass_args=True)
CONVERTER_HANDLER = CommandHandler('cash', convert)
TIME_HANDLER = DisableAbleCommandHandler("time", gettime)
REVERSE_HANDLER = DisableAbleCommandHandler(
    "reverse", reverse, pass_args=True, admin_ok=True)
TTS_HANDLER = DisableAbleCommandHandler('tts', tts, pass_args=True)

dispatcher.add_handler(APP_HANDLER)
dispatcher.add_handler(COVID_HANDLER)
dispatcher.add_handler(REVERSE_HANDLER)
dispatcher.add_handler(WALL_HANDLER)
dispatcher.add_handler(TIME_HANDLER)
dispatcher.add_handler(CONVERTER_HANDLER)
dispatcher.add_handler(TTS_HANDLER)
dispatcher.add_handler(UD_HANDLER)

__mod_name__ = "Extras"
__command_list__ = [
    "time",
    "cash",
    "wall",
    "reverse",
    "covid",
    "corona",
    "tts",
    "ud",
    "app"]
__handlers__ = [
    TIME_HANDLER,
    CONVERTER_HANDLER,
    WALL_HANDLER,
    REVERSE_HANDLER,
    COVID_HANDLER,
    TTS_HANDLER,
    UD_HANDLER,
    APP_HANDLER]
