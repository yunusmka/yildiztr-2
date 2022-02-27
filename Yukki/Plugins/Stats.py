import asyncio
import json
import logging
import multiprocessing
import platform
import re
import socket
import time
import uuid
from datetime import datetime
from sys import version as pyver

import psutil
from pymongo import MongoClient
from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import __version__ as pytgover

from config import (MONGO_DB_URI, MUSIC_BOT_NAME, STRING1, STRING2, STRING3,
                    STRING4, STRING5)
from Yukki import (ASS_CLI_1, ASS_CLI_2, ASS_CLI_3, ASS_CLI_4, ASS_CLI_5,
                   BOT_ID, MUSIC_BOT_NAME, SUDOERS, app, boottime)
from Yukki.Database import get_gbans_count, get_served_chats, get_sudoers
from Yukki.Inline import stats1, stats2, stats3, stats4, stats5, stats6, stats7
from Yukki.Plugins import ALL_MODULES
from Yukki.Utilities.ping import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - boottime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
**Uptime:** {get_readable_time((bot_uptime))}
**CPU:** {cpu}%
**RAM:** {mem}%
**Disk: **{disk}%"""
    return stats


@app.on_message(filters.command("stats") & ~filters.edited)
async def gstats(_, message):
    start = datetime.now()
    try:
        await message.delete()
    except:
        pass
    uptime = await bot_sys_stats()
    response = await message.reply_photo(
        photo="Utils/Query.jpg", caption="İstatistiklerini almak!"
    )
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    smex = f"""
[•]<u>**Genel İstatistikler**</u>

Ping: `⚡{resp} ms`
{uptime}
    """
    await response.edit_text(smex, reply_markup=stats1)
    return


@app.on_callback_query(
    filters.regex(
        pattern=r"^(sys_stats|sto_stats|bot_stats|Dashboard|mongo_stats|gen_stats|assis_stats|wait_stats)$"
    )
)
async def stats_markup(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "sys_stats":
        await CallbackQuery.answer("Sistem İstatistiklerini Almak...", show_alert=True)
        sc = platform.system()
        arch = platform.machine()
        p_core = psutil.cpu_count(logical=False)
        t_core = psutil.cpu_count(logical=True)
        try:
            cpu_freq = psutil.cpu_freq().current
            if cpu_freq >= 1000:
                cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
            else:
                cpu_freq = f"{round(cpu_freq, 2)}MHz"
        except:
            cpu_freq = "Unable to Fetch"
        cupc = "**Çekirdek Başına CPU Kullanımı:**\n"
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            cupc += f"Core {i}  : {percentage}%\n"
        cupc += "**Total CPU Usage:**\n"
        cupc += f"Tüm Çekirdek Kullanımı: {psutil.cpu_percent()}%\n"
        ram = (
            str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
        )
        bot_uptime = int(time.time() - boottime)
        uptime = f"{get_readable_time((bot_uptime))}"
        smex = f"""
[•]<u>**Sistem İstatistikleri**</u>

**{MUSIC_BOT_NAME} Uptime:** {uptime}
**Sistem İşlemi:** Online
**Peron:** {sc}
**Mimarlık:** {arch}
**Ram:** {ram}
**Python Sürümü:** {pyver.split()[0]}
**Pyrogram Sürümü:** {pyrover}
**PyTgCalls Sürümü:** {pytgover.__version__}

[•]<u>**CPU İstatistik**</u>

**Fiziksel Çekirdekler:** {p_core}
**Toplam Çekirdek sayısı:** {t_core}
**İşlemci Frekansı:** {cpu_freq}

{cupc}
"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats2)
    if command == "sto_stats":
        await CallbackQuery.answer(
            "Depolama İstatistiklerini Alma...", show_alert=True
        )
        hdd = psutil.disk_usage("/")
        total = hdd.total / (1024.0**3)
        total = str(total)
        used = hdd.used / (1024.0**3)
        used = str(used)
        free = hdd.free / (1024.0**3)
        free = str(free)
        smex = f"""
[•]<u>**Depolama İstatistikleri**</u>

**Kullanılabilir Depolama Alanı:** {total[:4]} GiB
**Kullanılan Depolama Alanı:** {used[:4]} GiB
**Depolama Sol:** {free[:4]} GiB"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats3)
    if command == "bot_stats":
        await CallbackQuery.answer("Bot İstatistiklerini Alma...", show_alert=True)
        served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
        blocked = await get_gbans_count()
        sudoers = await get_sudoers()
        modules_loaded = len(ALL_MODULES)
        j = 0
        for count, user_id in enumerate(sudoers, 0):
            try:
                user = await app.get_users(user_id)
                j += 1
            except Exception:
                continue
        smex = f"""
[•]<u>**Bot İstatistikleri**</u>

**Yüklenen Modüller:** {modules_loaded}
**GBanned Kullanıcıları:** {blocked}
**Sudo Kullanıcıları:** {j}
**Sunulan Sohbetler:** {len(served_chats)}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats4)
    if command == "mongo_stats":
        await CallbackQuery.answer(
            "MongoDB İstatistiklerini Alma...", show_alert=True
        )
        try:
            pymongo = MongoClient(MONGO_DB_URI)
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text(
                "Mongo DB istatistikleri alınamadı", reply_markup=stats5
            )
        try:
            db = pymongo.Yukki
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text(
                "Mongo DB istatistikleri alınamadı", reply_markup=stats5
            )
        call = db.command("dbstats")
        database = call["db"]
        datasize = call["dataSize"] / 1024
        datasize = str(datasize)
        storage = call["storageSize"] / 1024
        objects = call["objects"]
        collections = call["collections"]
        status = db.command("serverStatus")
        query = status["opcounters"]["query"]
        mver = status["version"]
        mongouptime = status["uptime"] / 86400
        mongouptime = str(mongouptime)
        provider = status["repl"]["tags"]["provider"]
        smex = f"""
[•]<u>**MongoDB İstatistikleri**</u>

**Mongo Çalışma Süresi:** {mongouptime[:4]} Days
**Sürüm:** {mver}
**Veritabanı:** {database}
**Sağlayıcı:** {provider}
**Veritabanı Boyutu:** {datasize[:6]} Mb
**Depolama:** {storage} Mb
**Koleksiyon:** {collections}
**Anahtar:** {objects}
**Toplam Sorgu Sayısı:** `{query}`"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats5)
    if command == "gen_stats":
        start = datetime.now()
        uptime = await bot_sys_stats()
        await CallbackQuery.answer(
            "Genel İstatistikleri Alma...", show_alert=True
        )
        end = datetime.now()
        resp = (end - start).microseconds / 1000
        smex = f"""
[•]<u>Genel İstatistikler</u>

**Ping:** `⚡{resp} ms`
{uptime}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats1)
    if command == "wait_stats":
        await CallbackQuery.answer()
    if command == "assis_stats":
        await CallbackQuery.answer(
            "Yardımcı İstatistikleri Alma...", show_alert=True
        )
        await CallbackQuery.edit_message_text(
            "Yardımcı İstatistikler alıyorum. Lütfen bekleyin...", reply_markup=stats7
        )
        groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
        groups_ub2 = channels_ub2 = bots_ub2 = privates_ub2 = total_ub2 = 0
        groups_ub3 = channels_ub3 = bots_ub3 = privates_ub3 = total_ub3 = 0
        groups_ub4 = channels_ub4 = bots_ub4 = privates_ub4 = total_ub4 = 0
        groups_ub5 = channels_ub5 = bots_ub5 = privates_ub5 = total_ub5 = 0

        if STRING1 != "None":
            async for i in ASS_CLI_1.iter_dialogs():
                t = i.chat.type
                total_ub += 1
                if t in ["supergroup", "group"]:
                    groups_ub += 1
                elif t == "channel":
                    channels_ub += 1
                elif t == "bot":
                    bots_ub += 1
                elif t == "private":
                    privates_ub += 1

        if STRING2 != "None":
            async for i in ASS_CLI_2.iter_dialogs():
                t = i.chat.type
                total_ub2 += 1
                if t in ["supergroup", "group"]:
                    groups_ub2 += 1
                elif t == "channel":
                    channels_ub2 += 1
                elif t == "bot":
                    bots_ub2 += 1
                elif t == "private":
                    privates_ub2 += 1

        if STRING3 != "None":
            async for i in ASS_CLI_3.iter_dialogs():
                t = i.chat.type
                total_ub3 += 1
                if t in ["supergroup", "group"]:
                    groups_ub3 += 1
                elif t == "channel":
                    channels_ub3 += 1
                elif t == "bot":
                    bots_ub3 += 1
                elif t == "private":
                    privates_ub3 += 1

        if STRING4 != "None":
            async for i in ASS_CLI_4.iter_dialogs():
                t = i.chat.type
                total_ub4 += 1
                if t in ["supergroup", "group"]:
                    groups_ub4 += 1
                elif t == "channel":
                    channels_ub4 += 1
                elif t == "bot":
                    bots_ub4 += 1
                elif t == "private":
                    privates_ub4 += 1

        if STRING5 != "None":
            async for i in ASS_CLI_5.iter_dialogs():
                t = i.chat.type
                total_ub5 += 1
                if t in ["supergroup", "group"]:
                    groups_ub5 += 1
                elif t == "channel":
                    channels_ub5 += 1
                elif t == "bot":
                    bots_ub5 += 1
                elif t == "private":
                    privates_ub5 += 1

        msg = "[•]<u>Yardımcı İstatistikleri</u>"
        if STRING1 != "None":
            msg += "\n\n<u>Asistan Bir:\n</u>"
            msg += f"""**Diyalog:** {total_ub}
**Grup:** {groups_ub}
**Kanal:** {channels_ub}
**Bot:** {bots_ub}
**Kullanıcı:** {privates_ub}"""

        if STRING2 != "None":
            msg += "\n\n<u>Asistan İki:\n</u>"
            msg += f"""**Diyalog:** {total_ub2}
**Grup:** {groups_ub2}
**Kanal:** {channels_ub2}
**Bots:** {bots_ub2}
**Kullanıcı:** {privates_ub2}"""

        if STRING3 != "None":
            msg += "\n\n<u>Assistant Three:\n</u>"
            msg += f"""**Dialogs:** {total_ub3}
**Grup:** {groups_ub3}
**Kanal:** {channels_ub3}
**Bot:** {bots_ub3}
**Kullanıcı:** {privates_ub3}"""

        if STRING4 != "None":
            msg += "\n\n<u>Assistant Four:\n</u>"
            msg += f"""**Dialogs:** {total_ub4}
**Grup:** {groups_ub4}
**Kanal:** {channels_ub4}
**Bot:** {bots_ub4}
**Kullanıcı:** {privates_ub4}"""

        if STRING5 != "None":
            msg += "\n\n<u>Assistant Five:\n</u>"
            msg += f"""**Dialogs:** {total_ub5}
**Grup:** {groups_ub5}
**Kanal:** {channels_ub5}
**Bot:** {bots_ub5}
**Kullanıcı:** {privates_ub5}"""
        await CallbackQuery.edit_message_text(msg, reply_markup=stats6)
