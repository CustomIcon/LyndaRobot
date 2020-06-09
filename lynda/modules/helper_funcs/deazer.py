from telegram import Bot, Update
def proper_trackdl(bot: Bot, update: Update, link, qual, msg, dir_):
    if 'spotify' in link:
        msg.reply_text("Trying to download song via Spotify Link 🥴")
        track = bot.download_trackspo(
            link,
            output=dir_,
            quality=qual,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        msg.reply_text("Now Uploading 📤")
        msg.send_audio(
            chat_id=msg.chat.id,
            audio=track
        )
    elif 'deezer' in link:
        msg.reply_text("Trying to download song via Deezer Link 🥴")
        track = bot.download_trackdee(
            link,
            output=dir_,
            quality=qual,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        msg.reply_text("Now Uploading 📤")
        msg.send_audio(
            chat_id=msg.chat.id,
            audio=track
        )


def batch_dl(bot: Bot, update: Update, link, qual, msg, dir_, u, allow_zip):
    if 'spotify' in link:
        if 'album/' in link:
            msg.reply_text("Trying to download album 🤧")
            if allow_zip:
                _, zip_ = bot.download_albumspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                msg.reply_text("Sending as Zip File 🗜")
                msg.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = bot.download_albumspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False)
                msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    msg.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )
        if 'playlist/' in link:
            msg.reply_text("Trying to download Playlist 🎶")
            if allow_zip:
                _, zip_ = bot.download_playlistspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                msg.reply_text("Sending as Zip 🗜")
                msg.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = bot.download_playlistspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    msg.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )

    if 'deezer' in link:
        if 'album/' in link:
            msg.reply_text("Trying to download album 🤧")
            if allow_zip:
                _, zip_ = bot.download_albumdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                msg.reply_text("Uploading as Zip File 🗜")
                msg.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = bot.download_albumdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    msg.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )
        elif 'playlist/' in link:
            msg.reply_text("Trying to download Playlist 🎶")
            if allow_zip:
                _, zip_ = bot.download_playlistdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                msg.reply_text("Sending as Zip File 🗜")
                msg.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = bot.download_playlistdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    bot.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )