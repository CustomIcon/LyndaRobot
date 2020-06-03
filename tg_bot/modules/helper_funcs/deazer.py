
def proper_trackdl(link, qual, msg, client, dir_, u):
    if 'spotify' in link:
        await msg.reply_text("Trying to download song via Spotify Link 🥴")
        track = client.download_trackspo(
            link,
            output=dir_,
            quality=qual,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        await msg.reply_text("Now Uploading 📤")
        await u.send_audio(
            chat_id=msg.chat.id,
            audio=track
        )
    elif 'deezer' in link:
        await msg.reply_text("Trying to download song via Deezer Link 🥴")
        track = client.download_trackdee(
            link,
            output=dir_,
            quality=qual,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        await msg.reply_text("Now Uploading 📤")
        await u.send_audio(
            chat_id=msg.chat.id,
            audio=track
        )


def batch_dl(link, qual, msg, client, dir_, u, allow_zip):
    if 'spotify' in link:
        if 'album/' in link:
            await msg.reply_text("Trying to download album 🤧")
            if allow_zip:
                _, zip_ = client.download_albumspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.reply_text("Sending as Zip File 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_albumspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False)
                await msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )
        if 'playlist/' in link:
            await msg.reply_text("Trying to download Playlist 🎶")
            if allow_zip:
                _, zip_ = client.download_playlistspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.reply_text("Sending as Zip 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_playlistspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                await msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )

    if 'deezer' in link:
        if 'album/' in link:
            await msg.reply_text("Trying to download album 🤧")
            if allow_zip:
                _, zip_ = client.download_albumdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.reply_text("Uploading as Zip File 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_albumdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                await msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )
        elif 'playlist/' in link:
            await msg.reply_text("Trying to download Playlist 🎶")
            if allow_zip:
                _, zip_ = client.download_playlistdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.reply_text("Sending as Zip File 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_playlistdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                await msg.reply_text("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )