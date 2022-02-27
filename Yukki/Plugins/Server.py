import asyncio
import math
import os
import dotenv
import random
import shutil
from datetime import datetime
from time import strftime, time

import heroku3
import requests
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import Client, filters
from pyrogram.types import Message

from config import (HEROKU_API_KEY, HEROKU_APP_NAME, UPSTREAM_BRANCH,
                    UPSTREAM_REPO)
from Yukki import LOG_GROUP_ID, MUSIC_BOT_NAME, SUDOERS, app
from Yukki.Database import get_active_chats, remove_active_chat, remove_active_video_chat
from Yukki.Utilities.heroku import is_heroku, user_input
from Yukki.Utilities.paste import isPreviewUp, paste_queue

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__MODULE__ = "Sunucu"
__HELP__ = f"""

**Not:**
**Sadece Sudo Kullanıcıları İçin**

/get_log
- Heroku'dan son 100 satırın günlüğünü alın.

/get_var
- Heroku veya .env'den yapılandırma var'ı almak.

/del_var
- Heroku veya .env üzerindeki herhangi bir var'ı silin.

/set_var [Var Adı] [Değer]
- Heroku veya .env üzerinde bir Var ayarlayın veya Var Güncelleştirin. Var'ı ve Değerini bir boşlukla ayırın.

/usage
- Dyno Kullanımını Alıp Alın.

/update
- Botunuzu Güncelleyin.

/restart 
- Botu Yeniden Başlat [Tüm indirmeler, önbellek, ham dosyalar da temizlenecek]. 
"""


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


@app.on_message(filters.command("get_log") & filters.user(SUDOERS))
async def log_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU UYGULAMASI ALGILANDI!</b>\n\nUygulamanızı güncellemek için `HEROKU_API_KEY` veya `HEROKU_APP_NAME` sırasıyla güncelleme yapın!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU UYGULAMASI ALGILANDI!</b>\n\n<b>Her ikisini de eklediğinizden emin olun</b> `HEROKU_API_KEY` **ve** `HEROKU_APP_NAME` <b>uzaktan güncelleştirebilmek için doğru şekilde güncelleyin!</b>"
            )
    else:
        return await message.reply_text("Sadece Heroku Uygulamaları İçin")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            " Lütfen Heroku API Anahtarınızın, Uygulama adınızın heroku'da doğru yapılandırıldığından emin olun"
        )
    data = happ.get_log()
    if len(data) > 1024:
        link = await paste_queue(data)
        url = link + "/index.txt"
        return await message.reply_text(
            f"İşte Uygulamanızın Günlüğü[{HEROKU_APP_NAME}]\n\n[Günlükleri ödemek için burayı tıklatın]({url})"
        )
    else:
        return await message.reply_text(data)


@app.on_message(filters.command("get_var") & filters.user(SUDOERS))
async def varget_(client, message):
    usage = "**Usage:**\n/get_var [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            return await message.reply_text(
                f"**Heroku Config:**\n\n**{check_var}:** `{heroku_config[check_var]}`"
            )
        else:
            return await message.reply_text("No such Var")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.get_key(path, check_var)
        if not output:
            return await message.reply_text("No such Var")
        else:
            return await message.reply_text(f".env:\n\n**{check_var}:** `{str(output)}`")


@app.on_message(filters.command("del_var") & filters.user(SUDOERS))
async def vardel_(client, message):
    usage = "**Usage:**\n/del_var [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Lütfen Heroku API Anahtarınızın, Uygulama adınızın heroku'da doğru yapılandırıldığından emin olun"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            await message.reply_text(
                f"**Heroku Var Silme:**\n\n`{check_var}` başarıyla silindi."
            )
            del heroku_config[check_var]
        else:
            return await message.reply_text(f"Yok böyle Var")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env bulunamadı.")
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await message.reply_text("Yok böyle Var")
        else:
            return await message.reply_text(f".env Var Silme:\n\n`{check_var}` başarıyla silindi. Bot dokunuşunu yeniden başlatmak için /restart komut.")


@app.on_message(filters.command("set_var") & filters.user(SUDOERS))
async def set_var(client, message):
    usage = "**Usage:**\n/set_var [Var Name] [Var Value]"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Lütfen Heroku API Anahtarınızın, Uygulama adınızın heroku'da doğru yapılandırıldığından emin olun"
            )
        heroku_config = happ.config()
        if to_set in heroku_config:
            await message.reply_text(
                f"**Heroku Var Updation:**\n\n`{to_set}` has been updated successfully. Bot will Restart Now."
            )
        else:
            await message.reply_text(
                f"Added New Var with name `{to_set}`. Bot will Restart Now."
            )
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            return await message.reply_text(f"**.env Var Updation:**\n\n`{to_set}`has been updated successfully. To restart the bot touch /restart command.")
        else:
            return await message.reply_text(f"**.env dəyişən əlavə edilməsi:**\n\n`{to_set}` has been added sucsessfully. To restart the bot touch /restart command.")


@app.on_message(filters.command("usage") & filters.user(SUDOERS))
async def usage_dynos(client, message):
    ### Credits CatUserbot
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
    else:
        return await message.reply_text("Only for Heroku Apps")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
        )
    dyno = await message.reply_text("Checking Heroku Usage. Please Wait")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
**DYNO USAGE**

<u>Usage:</u>
Total Used: `{AppHours}`**h**  `{AppMinutes}`**m**  [`{AppPercentage}`**%**]

<u>Remaining Quota:</u>
Total Left: `{hours}`**h**  `{minutes}`**m**  [`{percentage}`**%**]"""
    return await dyno.edit(text)


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
    response = await message.reply_text("𝗠𝗲𝘃𝗰𝘂𝘁 𝗴𝘂̈𝗻𝗰𝗲𝗹𝗹𝗲𝗺𝗲𝗹𝗲𝗿𝗶 𝗸𝗼𝗻𝘁𝗿𝗼𝗹 𝗲𝗱𝗶𝘆𝗼𝗿𝘂𝗺...")
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit("Git Command Error")
    except InvalidGitRepositoryError:
        return await response.edit("Invalid Git Repsitory")
    to_exc = f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]  # main git repository
    for checks in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit("𝗕𝗼𝘁 𝗴𝘂̈𝗻𝗰𝗲𝗹!")
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[
            (format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4
        ],
    )
    for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: [{info.summary}]({REPO_}/commit/{info}) by -> {info.author}</b>\n\t\t\t\t<b>➥ Commited on:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    _update_response_ = "<b>A new update is available for the Bot!</b>\n\n➣ Pushing Updates Now</code>\n\n**<u>Updates:</u>**\n\n"
    _final_updates_ = _update_response_ + updates
    if len(_final_updates_) > 4096:
        link = await paste_queue(updates)
        url = link + "/index.txt"
        nrs = await response.edit(
            f"<b>A new update is available for the Bot!</b>\n\n➣ Pushing Updates Now</code>\n\n**<u>Updates:</u>**\n\n[Click Here to checkout Updates]({url})"
        )
    else:
        nrs = await response.edit(
            _final_updates_, disable_web_page_preview=True
        )
    os.system("git stash &> /dev/null && git pull")
    if await is_heroku():
        try:
            await response.edit(
                f"{nrs.text}\n\nBot was updated successfully on Heroku! Now, wait for 2 - 3 mins until the bot restarts!"
            )
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(
                f"{nrs.text}\n\nSomething went wrong while initiating reboot! Please try again later or check logs for more info."
            )
            return await app.send_message(
                LOG_GROUP_ID,
                f"AN EXCEPTION OCCURRED AT #UPDATER DUE TO: <code>{err}</code>",
            )
    else:
        await response.edit(
            f"{nrs.text}\n\nBot was updated successfully! Now, wait for 1 - 2 mins until the bot reboots!"
        )
        os.system("pip3 install -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && bash start")
        exit()
    return


@app.on_message(filters.command("restart") & filters.user(SUDOERS))
async def restart_(_, message):
    response = await message.reply_text("𝗬𝗲𝗻𝗶𝗱𝗲𝗻 𝗕𝗮𝘀̧𝗹𝗮𝘁𝗶𝗹𝗶𝘆𝗼𝗿....")
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to restart your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to restart remotely!</b>"
            )
        try:
            served_chats = []
            try:
                chats = await get_active_chats()
                for chat in chats:
                    served_chats.append(int(chat["chat_id"]))
            except Exception as e:
                pass
            for x in served_chats:
                try:
                    await app.send_message(
                        x,
                        f"{MUSIC_BOT_NAME} Sadece kendini yeniden başlatıldı. Sorunlar için üzgünüm.\n\n10-15 saniye sonra tekrar oynamaya başlayın.",
                    )
                    await remove_active_chat(x)
                    await remove_active_video_chat(x)
                except Exception:
                    pass
            heroku3.from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME].restart()
            await response.edit(
                "**Heroku Yeniden Başlatma**\n\n𝗬𝗲𝗻𝗶𝗱𝗲𝗻 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗺𝗮 𝗯𝗮𝘀̧𝗮𝗿𝗶𝘆𝗹𝗮 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗶𝗹𝗱𝗶! 𝗕𝗼𝘁 𝘆𝗲𝗻𝗶𝗱𝗲𝗻 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗶𝗹𝗮𝗻𝗮 𝗸𝗮𝗱𝗮𝗿 𝟭-𝟮 𝗱𝗮𝗸𝗶𝗸𝗮 𝗯𝗲𝗸𝗹𝗲𝘆𝗶𝗻."
            )
            return
        except Exception as err:
            await response.edit(
                "Yeniden başlatmayı başlatırken bir şeyler ters gitti! Lütfen daha sonra tekrar deneyin veya daha fazla bilgi için günlükleri kontrol edin."
            )
            return
    else:
        served_chats = []
        try:
            chats = await get_active_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
        except Exception as e:
            pass
        for x in served_chats:
            try:
                await app.send_message(
                    x,
                    f"{MUSIC_BOT_NAME} has just restarted herself. Sorry for the issues.\n\nStart playing after 10-15 seconds again.",
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except Exception:
                pass
        A = "downloads"
        B = "raw_files"
        C = "cache"
        D = "search"
        try:
            shutil.rmtree(A)
            shutil.rmtree(B)
            shutil.rmtree(C)
            shutil.rmtree(D)
        except:
            pass
        await asyncio.sleep(2)
        try:
            os.mkdir(A)
        except:
            pass
        try:
            os.mkdir(B)
        except:
            pass
        try:
            os.mkdir(C)
        except:
            pass
        try:
            os.mkdir(D)
        except:
            pass
        await response.edit(
            "𝗬𝗲𝗻𝗶𝗱𝗲𝗻 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗺𝗮 𝗯𝗮𝘀̧𝗮𝗿𝗶𝘆𝗹𝗮 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗶𝗹𝗱𝗶! 𝗕𝗼𝘁 𝘆𝗲𝗻𝗶𝗱𝗲𝗻 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗶𝗹𝗮𝗻𝗮 𝗸𝗮𝗱𝗮𝗿 𝟭-𝟮 𝗱𝗮𝗸𝗶𝗸𝗮 𝗯𝗲𝗸𝗹𝗲𝘆𝗶𝗻."
        )
        os.system(f"kill -9 {os.getpid()} && bash start")
