from lynda.modules.helper_funcs.telethn.chatstatus import user_is_admin 
from lynda.modules.helper_funcs.telethn.chatstatus import can_delete_messages
from lynda.lyn import lyndabot


@lyndabot(pattern="^/purge")
async def purge_messages(event):
    if event.from_id == None:
        return

    if not await user_is_admin(user_id=event.from_id, message=event):
        await event.reply(event.chat_id, "Only Admins are allowed to use this command")
        return

    if not await can_delete_messages(message=event):
        await event.reply(event.chat_id, "Can't seem to purge the message")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply(event.chat_id, "I Can't Purge nothing")
        return
    msgs = []
    msg_id = msg.id
    delete_to = event.message.id - 1
    await event.client.delete_messages(event.chat_id, event.message.id)

    msgs.append(event.reply_to_msg_id)
    for m_id in range(delete_to, msg_id - 1, -1):
        msgs.append(m_id)
        if len(msgs) == 100:
            await event.client.delete_messages(event.chat_id, msgs)
            msgs = []

    await event.client.delete_messages(event.chat_id, msgs)
    text = (event.chat_id, "Purged Successfully!")
    await event.respond(text, parse_mode='markdown')


@lyndabot(pattern="^/del$")
async def delete_messages(event):
    if event.from_id == None:
        return

    if not await user_is_admin(user_id=event.from_id, message=event):
        await event.reply(event.chat_id, "Only Admins are allowed to use this command")
        return

    if not await can_delete_messages(message=event):
        await event.reply(event.chat_id, "Can't seem to delete this?")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply(event.chat_id, "I can't delete nothing")
        return
    currentmsg = event.message
    chat = await event.get_input_chat()
    delall = [msg, currentmsg]
    await event.client.delete_messages(chat, delall)



__help__ = """
*Admin only:*
 - /del: deletes the message you replied to
 - /purge: deletes all messages between this and the replied to message.
 - /purge <integer X>: deletes the replied message, and X messages following it if replied to a message.
"""

__mod_name__ = "Purges"