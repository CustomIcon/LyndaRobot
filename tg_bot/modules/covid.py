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
        #reply_text = f"**Global Totals**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
        last_updated = datetime.datetime.fromtimestamp(r['updated']/1000).strftime("%Y-%m-%d %I:%M:%S")
        ac = PrettyTable()
        ac.header = False
        
        ac.title = "Global Statistics"
        ac.add_row(["Cases", f"{r['cases']:,}"])
        ac.add_row(["Cases Today", f"{r['todayCases']:,}"])
        ac.add_row(["Deaths", f"{r['deaths']:,}"])
        ac.add_row(["Deaths Today", f"{r['todayDeaths']:,}"])
        ac.add_row(["Recovered", f"{r['recovered']:,}"])
        ac.add_row(["Active", f"{r['active']:,}"])
        ac.add_row(["Critical", f"{r['critical']:,}"])
        ac.add_row(["Cases/Million", f"{r['casesPerOneMillion']:,}"])
        ac.add_row(["Deaths/Million", f"{r['deathsPerOneMillion']:,}"])
        ac.add_row(["Tests", f"{r['tests']:,}"])
        ac.add_row(["Tests/Million", f"{r['testsPerOneMillion']:,}"])
        #ac.add_row(["Affected Countries", f"{r['affectedCountries']:,}"])
        ac.align = "l"
        reply_text = f"‎\n```{str(ac)}```\nLast updated on: {last_updated}"
    else:
        variabla = text[1]
        r = requests.get(f"https://corona.lmao.ninja/v2/countries/{variabla}").json()
        #reply_text = f"**Cases for {r['country']}**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
        last_updated = datetime.datetime.fromtimestamp(r['updated']/1000).strftime("%Y-%m-%d %I:%M:%S")
        country = r['countryInfo']['iso3'] if len(r['country']) > 12 else r['country']
        cc = PrettyTable()
        cc.header = False
        country = r['countryInfo']['iso3'] if len(r['country']) > 12 else r['country']
        cc.title = f"Corona Cases in {country}"
        cc.add_row(["Cases", f"{r['cases']:,}"])
        cc.add_row(["Cases Today", f"{r['todayCases']:,}"])
        cc.add_row(["Deaths", f"{r['deaths']:,}"])
        cc.add_row(["Deaths Today", f"{r['todayDeaths']:,}"])
        cc.add_row(["Recovered", f"{r['recovered']:,}"])
        cc.add_row(["Active", f"{r['active']:,}"])
        cc.add_row(["Critical", f"{r['critical']:,}"])
        cc.add_row(["Cases/Million", f"{r['casesPerOneMillion']:,}"])
        cc.add_row(["Deaths/Million", f"{r['deathsPerOneMillion']:,}"])
        cc.add_row(["Tests", f"{r['tests']:,}"])
        cc.add_row(["Tests/Million", f"{r['testsPerOneMillion']:,}"])
        cc.align = "l"
        reply_text = f"‎\n```{str(cc)}```\nLast updated on: {last_updated}"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

__help__ = """
 - /covid To get Global data
 - /covid <country> To get data of a country
"""

COVID_HANDLER = DisableAbleCommandHandler(["covid", "corona"], covid)

dispatcher.add_handler(COVID_HANDLER)

__mod_name__ = "Corona Info"