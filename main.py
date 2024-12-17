import os
import sys
import time
import asyncio
import tempfile
import requests
import json
import subprocess
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyromod import listen
from aiohttp import ClientSession
from logger import logging
from config import *
from helper import download_video, send_vid, download

bot = Client("bot", bot_token="", api_id=22609670, api_hash="3506d8474ad1f4f5e79b7c52a5c3e88d")


@bot.on_message(filters.command(["start"]) & filters.user(ADMINS))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"HELLO I AM TXT DOWNLOADER BOT MADE BY CR CHOUDHARY [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nPress /BOSS")


@bot.on_message(filters.command("stop") & filters.user(ADMINS))
async def restart_handler(_, m):
    await m.reply_text("**STOPPED**🛑🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["BOSS"]) & filters.user(ADMINS))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"**Hey [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nSend txt 🗃️ file**")
    input: Message = await bot.listen(editable.chat.id)
    if input.document:
        x = await input.download()
        await bot.send_document(-1002374822952, x)
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"

        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                links.append(i.split("://", 1))
            os.remove(x)  # Delete the file after reading its contents
        except:
            await m.reply_text("Invalid file input.🥲😒🤦🏻")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))

    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send d for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        else:
            res = "UN"
    except Exception:
        res = "UN"

    await editable.edit("**Enter Your Name or send `de` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == 'de':
        CR = credit
    else:
        CR = raw_text3

    await editable.edit("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            # Clean filename for download
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            # Command to download video
            cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            try:
                # Preparing caption for the media
                cc = f"""╭━━━━━━━━━━━━━━━━━━━━━╮
💫 **𝐕𝐈𝐃𝐄𝐎 𝐈𝐃** : {str(count).zfill(3)}
╰━━━━━━━━━━━━━━━━━━━━━╮
📁 **𝐓𝐈𝐓𝐋𝐄** : {name1} ({res})

📚 **𝐂𝐎𝐔𝐑𝐒𝐄** : {b_name}  
📥 **𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃 𝐁𝐘** : {CR}

🔗 [**𝐉𝐎𝐈𝐍 𝐌𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋**](https://t.me/TARGETALLCOURSE)
"""

                cc1 = f"""╭━━━━━━━━━━━━━━━━━━━━━╮
💫 **𝐏𝐃𝐅 𝐈𝐃** : {str(count).zfill(3)}
╰━━━━━━━━━━━━━━━━━━━━━╮
📁 **𝐓𝐈𝐓𝐋𝐄** : {name1}

📚 **𝐂𝐎𝐔𝐑𝐒𝐄** : {b_name}  
📥 **𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃 𝐁𝐘** : {CR}

🔗 [**𝐉𝐎𝐈𝐍 𝐌𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋**](https://t.me/targetallcourse)
"""

                # Start downloading the video
                prog = await m.reply_text(f"**Downloading:-**\n\n** Video Name :-** `{name}\nQuality - {raw_text2}`\n**link:**`{url}`\n\n **bot made by cr choudhary ❤️**")
                res_file = await download_video(url, cmd, name)
                filename = res_file

                # After download, send video and clean up the file
                await prog.delete(True)
                await send_vid(bot, m, cc, filename, thumb, name)

                # Clean up the downloaded video file to save storage
                os.remove(filename)

                # Delete the thumbnail file if it was downloaded
                if os.path.exists('thumb.jpg'):
                    os.remove('thumb.jpg')

                # Increase the count
                count += 1

            except Exception as e:
                # Handle failure
                if ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        await copy.copy(chat_id=-1002374822952)

                        # Clean up the downloaded PDF file to save storage
                        os.remove(f'{name}.pdf')

                        count += 1
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                    except Exception as ex:
                        await m.reply_text(f"**This #Failed File is not Counted**\n**Skipping to next file.**")
                        continue

    except Exception as ex:
        await m.reply_text(f"Error processing links: {ex}")

    # Cleanup and final message
    await m.reply_text("**DONE BOSS 📚** 🎉")

    # Clean up any temporary or unprocessed files (e.g., thumbnail, logs, etc.)
    if os.path.exists('thumb.jpg'):
        os.remove('thumb.jpg')

    # Optionally, clear any other cache or temp files from yt-dlp
    temp_cache_dir = './yt-dlp_cache'
    if os.path.exists(temp_cache_dir):
        for file in os.listdir(temp_cache_dir):
            file_path = os.path.join(temp_cache_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                os.rmdir(file_path)  # Delete any empty directories

bot.run()
