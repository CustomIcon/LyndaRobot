from typing import Optional, List
from telegram import Update
from telegram.ext import CallbackContext
from lynda import dispatcher
from lynda.modules.disable import DisableAbleCommandHandler
import wikipedia


def wiki(update: Update, context: CallbackContext):
    args = context.args
    reply = " ".join(args)
    summary = '{} {}'
    update.message.reply_text(
        summary.format(
            wikipedia.summary(
                reply,
                sentences=3),
            wikipedia.page(reply).url))


__help__ = """
-> `/wiki` text
Returns search from wikipedia for the input text
"""
__mod_name__ = "Wikipedia"
WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki, pass_args=True)
dispatcher.add_handler(WIKI_HANDLER)
