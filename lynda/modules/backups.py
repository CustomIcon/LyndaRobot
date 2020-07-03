import json
from io import BytesIO

from telegram import Bot, Update
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async

from lynda import dispatcher, LOGGER
from lynda.__main__ import DATA_IMPORT
from lynda.modules.helper_funcs.chat_status import user_admin


@run_async
@user_admin
def import_data(bot: Bot, update: Update):
    msg = update.effective_message
    chat = update.effective_chat
    # TODO: allow uploading doc with command, not just as reply
    # only work with a doc
    if msg.reply_to_message and msg.reply_to_message.document:
        try:
            file_info = bot.get_file(msg.reply_to_message.document.file_id)
        except BadRequest:
            msg.reply_text(
                "Try downloading and reuploading the file as yourself before importing - this one seems "
                "to be iffy!")
            return

        with BytesIO() as file:
            file_info.download(out=file)
            file.seek(0)
            data = json.load(file)

        # only import one group
        if len(data) > 1 and str(chat.id) not in data:
            msg.reply_text(
                "Theres more than one group here in this file, and none have the same chat id as this group "
                "- how do I choose what to import?")
            return

        # Select data source
        if str(chat.id) in data:
            data = data[str(chat.id)]['hashes']
        else:
            data = data[list(data.keys())[0]]['hashes']

        try:
            for mod in DATA_IMPORT:
                mod.__import_data__(str(chat.id), data)
        except Exception:
            msg.reply_text(
                "An exception occured while restoring your data. The process may not be complete. If "
                "you're having issues with this, message @Aman_Ahmed with your backup file so the "
                "issue can be debugged. My owners would be happy to help, and every bug "
                "reported makes me better! Thanks! :)")
            LOGGER.exception(
                "Import for chatid %s with name %s failed.", str(
                    chat.id), str(
                    chat.title))
            return

        # TODO: some of that link logic
        # NOTE: consider default permissions stuff?
        msg.reply_text("Backup fully imported. Welcome back! :D")


@run_async
@user_admin
def export_data(_bot: Bot, update: Update):
    msg = update.effective_message
    msg.reply_text("Doesn't work yet.")


__help__ = """
*Admin only:*
 - /import: reply to a group butler backup file to import as much as possible, making the transfer super simple! Note \
that files/photos can't be imported due to telegram restrictions.
 - /export: !!! This isn't a command yet, but should be coming soon!
"""

IMPORT_HANDLER = CommandHandler("import", import_data)
EXPORT_HANDLER = CommandHandler("export", export_data)

dispatcher.add_handler(IMPORT_HANDLER)
dispatcher.add_handler(EXPORT_HANDLER)

__mod_name__ = "Backups"
__handlers__ = [IMPORT_HANDLER, EXPORT_HANDLER]
