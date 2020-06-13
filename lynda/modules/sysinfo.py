
# Rikka Takanashi   
# Copyright (C) 2019  MadiNyan https://github.com/MadiNyan
import platform
import cpuinfo
import psutil
from uptime import uptime

from telegram import ChatAction
from telegram import Update, Bot
from telegram.ext import run_async
from lynda.modules.helper_funcs.chat_status import dev_plus

from lynda import dispatcher
from lynda.modules.disable import DisableAbleCommandHandler

def seconds_to_str(seconds):
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{} day(s), {:02} hours, {:02} minutes, {:02} seconds".format(days, hours, minutes, seconds)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

@dev_plus
@run_async
def sysinfo(bot: Bot, update: Update):
    update.message.chat.send_action(ChatAction.TYPING)
    uname = platform.uname()
    a = "="*10, " 💻 System Info ", "="*9
    sys_header = "".join(a)
    sys_info = "{}\n\nSystem: {}\nNode Name: {}\nVersion: {}\n".format(sys_header, uname.system, uname.node, uname.version)
    b = "="*14, " Uptime ", "="*13
    upt_header = "".join(b)
    f = int(uptime())
    pcuptime = seconds_to_str(f)
    up = "{}\n\nUptime: {}\n".format(upt_header, pcuptime)
    c = "="*15, " CPU ", "="*15
    cpu_header = "".join(c)
    cpumodel = cpuinfo.get_cpu_info()['brand']
    cpufreq = psutil.cpu_freq()
    cpu_info = "{}\n\n{}\nPhysical cores: {}\nTotal cores: {}\nMax Frequency: {:.2f} Mhz\nCurrent Frequency: {:.2f} Mhz\nCPU Usage: {}%\n".format(
                cpu_header, cpumodel, psutil.cpu_count(logical=False), psutil.cpu_count(logical=True), cpufreq.max, cpufreq.current, psutil.cpu_percent(percpu=False, interval=1))
    d = "="*15, " RAM ", "="*15
    ram_header = "".join(d)
    svmem = psutil.virtual_memory()
    ram_info = "{}\n\nTotal: {}\nAvailable: {} ({:.2f}%)\nUsed: {} ({:.2f}%)\n".format(
                ram_header, get_size(svmem.total), get_size(svmem.available), 100-svmem.percent, get_size(svmem.used), svmem.percent)
    server_status = "```\n{}\n{}\n{}\n{}\n```".format(sys_info, up, cpu_info, ram_info)
    update.message.reply_text(server_status, parse_mode="Markdown")

# __help__ = """
#  **Dev Only!**
#  - /sysinfo - Gives information about bot hosted server.
# """
__mod_name__ = "System Info"
SYSINFO_HANDLER = DisableAbleCommandHandler("sysinfo", sysinfo)
dispatcher.add_handler(SYSINFO_HANDLER)