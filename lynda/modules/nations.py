import html
import json
import os
from typing import List, Optional

from telegram import Update, ParseMode, TelegramError
from telegram.ext import CommandHandler, run_async, CallbackContext
from telegram.utils.helpers import mention_html

from lynda import dispatcher, WHITELIST_USERS, SARDEGNA_USERS, SUPPORT_USERS, SUDO_USERS, DEV_USERS, OWNER_ID
from lynda.modules.helper_funcs.chat_status import whitelist_plus, dev_plus, sudo_plus
from lynda.modules.helper_funcs.extraction import extract_user
from lynda.modules.log_channel import gloggable

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), 'lynda/elevated_users.json')


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# I added extra new lines
nations = """ Lynda has bot access levels we call as *"Nation Levels"* just like Kigyo
\n*Eagle Union* - Devs who can access the bots server and can execute, edit, modify bot code. Can also manage other Nations
\n*God* - Only one exists, bot owner.
Owner has complete bot access, including bot adminship in chats Lynda is at.
\n*Royals* - Have super user access, can gban, manage Nations lower than them and are admins in Lynda.
\n*Sakuras* - Have access go globally ban users across Lynda.
\n*Sardegnas* - Same as Neptunians but can unban themselves if banned.
\n*Neptunians* - Cannot be banned, muted flood kicked but can be manually banned by admins.
\n*Disclaimer*: The Nation levels in Lynda are there for troubleshooting, support, banning potential scammers.
Report abuse or ask us more on these at [Lynda Eagle Support](https://t.me/LyndaEagleSupport).
"""
# do not async, not a handler


def send_nations(update):
    update.effective_message.reply_text(
        nations,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True)


@run_async
@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot = context.bot
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        message.reply_text("This member is already a Royal Nation")
        return ""

    if user_id in SUPPORT_USERS:
        rt += "Requested HA to promote a Sakura Nation to Royal."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        rt += "Requested HA to promote a Neptunia Nation to Royal."
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    data['sudos'].append(user_id)
    SUDO_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        "\nSuccessfully set Nation level of {} to Royal!".format(
            user_member.first_name))

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addsupport(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot = context.bot
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "Requested HA to deomote this Royal to Sakura"
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        message.reply_text("This user is already a Sakura Nation.")
        return ""

    if user_id in WHITELIST_USERS:
        rt += "Requested HA to promote this Neptunia Nation to Sakura"
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    data['supports'].append(user_id)
    SUPPORT_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a Sakura Nation!")

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot = context.bot
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "This member is a Royal Nation, Demoting to Neptunia."
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        rt += "This user is already a Sakura Nation, Demoting to Neptunia."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        message.reply_text("This user is already a Neptunia Nation.")
        return ""

    data['whitelists'].append(user_id)
    WHITELIST_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a Neptunia Nation!")

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)} \n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addSardegna(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot = context.bot
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "This member is a Royal Nation, Demoting to Sardegna."
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        rt += "This user is already a Sakura Nation, Demoting to Sardegna."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        rt += "This user is already a Neptunia Nation, Demoting to Sardegna."
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    if user_id in SARDEGNA_USERS:
        message.reply_text("This user is already a Sardegna.")
        return ""

    data['Sardegnas'].append(user_id)
    SARDEGNA_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a Sardegna Nation!")

    log_message = (
        f"#SARDEGNA\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)} \n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot = context.bot
    message = update.effective_message
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""
    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)
    if user_id in SUDO_USERS:
        message.reply_text("Requested HA to demote this user to Civilian")
        SUDO_USERS.remove(user_id)
        data['sudos'].remove(user_id)
        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)
        user = update.effective_user
        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")
        chat = update.effective_chat
        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(
                html.escape(chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a Royal Nation!")
        return ""


@run_async
@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot = context.bot
    message = update.effective_message
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUPPORT_USERS:
        message.reply_text("Requested HA to demote this user to Civilian")
        SUPPORT_USERS.remove(user_id)
        data['supports'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        user = update.effective_user
        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

        chat = update.effective_chat

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a Sakura level Nation!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot = context.bot
    message = update.effective_message
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WHITELIST_USERS:
        message.reply_text("Demoting to normal user")
        WHITELIST_USERS.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        user = update.effective_user
        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

        chat = update.effective_chat

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Neptunia Nation!")
        return ""


@run_async
@sudo_plus
@gloggable
def removeSardegna(update: Update, context: CallbackContext) -> str:
    args = context.args
    bot= context.bot
    message = update.effective_message
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SARDEGNA_USERS:
        message.reply_text("Demoting to normal user")
        SARDEGNA_USERS.remove(user_id)
        data['Sardegnas'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        user = update.effective_user
        log_message = (
            f"#UNSARDEGNA\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

        chat = update.effective_chat

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Sardegna Nation!")
        return ""


@run_async
@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Neptunia Nations 🐺:</b>\n"
    for each_user in WHITELIST_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def Sardegnalist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Sardegna Nations 🐯:</b>\n"
    for each_user in SARDEGNA_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Sakura Nations 👹:</b>\n"
    for each_user in SUPPORT_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(SUDO_USERS) - set(DEV_USERS))
    reply = "<b>Known Royal Nations 🐉:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>Eagle Union Members ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = """
-> `/Eagle`
Lists all Eagle Union members.
-> `/Royals`
Lists all Royal Nations.
-> `/Sakuras`
Lists all Sakura Nations.
-> `/Sardegnas`
Lists all Sardegnas Nations.
-> `/Neptunians`
Lists all Neptunia Nations.

──「 *Note:* 」──
These commands list users with special bot priveleges and can only be used by them.
You can visit @YorktownEagleUnion or @LyndaEagleSupport to query more about these.
"""

SUDO_HANDLER = CommandHandler(("addsudo", "addRoyal"), addsudo, pass_args=True)
SUPPORT_HANDLER = CommandHandler(
    ("addsupport", "addSakura"), addsupport, pass_args=True)
SARDEGNA_HANDLER = CommandHandler(("addSardegna"), addSardegna, pass_args=True)
WHITELIST_HANDLER = CommandHandler(
    ("addwhitelist", "addNeptunia"), addwhitelist, pass_args=True)
UNSUDO_HANDLER = CommandHandler(
    ("removesudo", "removeRoyal"), removesudo, pass_args=True)
UNSUPPORT_HANDLER = CommandHandler(
    ("removesupport", "removeSakura"), removesupport, pass_args=True)
UNSARDEGNA_HANDLER = CommandHandler(
    ("removeSardegna"),
    removeSardegna,
    pass_args=True)
UNWHITELIST_HANDLER = CommandHandler(
    ("removewhitelist",
    "removeNeptunia"),
    removewhitelist,
    pass_args=True)

WHITELISTLIST_HANDLER = CommandHandler(
    ["whitelistlist", "Neptunians"], whitelistlist)
SARDEGNALIST_HANDLER = CommandHandler(["Sardegnas"], Sardegnalist)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "Sakuras"], supportlist)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "Royals"], sudolist)
DEVLIST_HANDLER = CommandHandler(["devlist", "Eagle"], devlist)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(SARDEGNA_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNSARDEGNA_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(SARDEGNALIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Nations"
__handlers__ = [
    SUDO_HANDLER,
    SUPPORT_HANDLER,
    SARDEGNA_HANDLER,
    WHITELIST_HANDLER,
    UNSUDO_HANDLER,
    UNSUPPORT_HANDLER,
    UNSARDEGNA_HANDLER,
    UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER,
    SARDEGNALIST_HANDLER,
    SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER,
    DEVLIST_HANDLER]
