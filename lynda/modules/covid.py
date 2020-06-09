import requests
import datetime
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from prettytable import PrettyTable

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler

@run_async
def covid(bot: Bot, update: Update):
    message = update.effective_message
    text = message.text.split(' ', 1)
    if len(text) == 1:
        r = requests.get(f"https://corona.lmao.ninja/v2/all").json()
        reply_text = f"**Global Totals** 🦠\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    else:
        variabla = text[1]
        r = requests.get(f"https://corona.lmao.ninja/v2/countries/{variabla}").json()
        reply_text = f"**Cases for {r['country']} 🦠**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

__help__ = """
 - /covid To get Global data
 - /covid <country> To get data of a country
"""

COVID_HANDLER = DisableAbleCommandHandler(["covid", "corona"], covid)

dispatcher.add_handler(COVID_HANDLER)

__mod_name__ = "Corona Info"