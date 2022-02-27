import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto,
                            KeyboardButton, Message, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove, Voice)
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch

from Yukki import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from Yukki.Core.PyTgCalls.Converter import convert
from Yukki.Core.PyTgCalls.Downloader import download
from Yukki.Database import (get_active_video_chats, get_video_limit,
                            is_active_video_chat, is_on_off)
from Yukki.Decorators.assistant import AssistantAdd
from Yukki.Decorators.checker import checker
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (choose_markup, livestream_markup, playlist_markup,
                          search_markup, search_markup2, stream_quality_markup,
                          url_markup, url_markup2)
from Yukki.Utilities.changers import seconds_to_min, time_to_seconds
from Yukki.Utilities.chat import specialfont_to_normal
from Yukki.Utilities.theme import check_theme
from Yukki.Utilities.thumbnails import gen_thumb
from Yukki.Utilities.url import get_url
from Yukki.Utilities.videostream import start_live_stream, start_video_stream
from Yukki.Utilities.youtube import (get_m3u8, get_yt_info_id,
                                     get_yt_info_query,
                                     get_yt_info_query_slider)

loop = asyncio.get_event_loop()

__MODULE__ = "oynat"
__HELP__ = f"""

/oynat [Herhangi bir Ses veya Videoyu Yanıtlayın] veya [YT Bağlantısı] veya [Müzik Adı]
- Sesli Sohbette Ses + Video Akışı

/bul [Youtube URL'si veya Arama Sorgusu] 
- Belirli bir sorguyu ses veya video biçiminde indirme.
"""


@app.on_callback_query(filters.regex(pattern=r"Yukki"))
async def choose_playmode(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkınızı Arayın.", show_alert=True
        )
    buttons = choose_markup(videoid, duration, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"Choose"))
async def quality_markup(_, CallbackQuery):
    limit = await get_video_limit(141414)
    if not limit:
        await CallbackQuery.message.delete()
        return await CallbackQuery.message.reply_text(
            "**Görüntülü Aramalar İçin Sınır Tanımlanmadı**\n\nBot'ta İzin Verilen Maksimum Görüntülü Arama Sayısı İçin Bir Sınır Ayarlama /set_video_limit [Yalnızca Sudo Kullanıcıları]"
        )
    count = len(await get_active_video_chats())
    if int(count) == int(limit):
        if await is_active_video_chat(CallbackQuery.message.chat.id):
            pass
        else:
            return await CallbackQuery.answer(
                "Pardon! Bot, CPU aşırı yükleme sorunları nedeniyle yalnızca sınırlı sayıda görüntülü aramaya izin verir. Diğer sohbetler şu anda görüntülü arama kullanıyor. Sese geçmeyi deneyin veya daha sonra yeniden deneyin",
                show_alert=True,
            )
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    try:
        read1 = db_mem[CallbackQuery.message.chat.id]["live_check"]
        if read1:
            return await CallbackQuery.answer(
                "Canlı Yayın Oynatıyor... Müzik çalmak için durdurun",
                show_alert=True,
            )
        else:
            pass
    except:
        pass
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkınızı Arayın.", show_alert=True
        )
    buttons = stream_quality_markup(videoid, duration, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"LiveStream"))
async def Live_Videos_Stream(_, CallbackQuery):
    limit = await get_video_limit(141414)
    if not limit:
        await CallbackQuery.message.delete()
        return await CallbackQuery.message.reply_text(
            "**Görüntülü Aramalar İçin Sınır Tanımlanmadı**\n\nBot'ta İzin Verilen Maksimum Görüntülü Arama Sayısı İçin Bir Sınır Ayarlama /set_video_limit [Yalnızca Sudo Kullanıcıları]"
        )
    count = len(await get_active_video_chats())
    if int(count) == int(limit):
        if await is_active_video_chat(CallbackQuery.message.chat.id):
            pass
        else:
            return await CallbackQuery.answer(
                "Pardon! Bot, CPU aşırı yükleme sorunları nedeniyle yalnızca sınırlı sayıda görüntülü aramaya izin verir. Diğer sohbetler şu anda görüntülü arama kullanıyor. Sese geçmeyi deneyin veya daha sonra yeniden deneyin",
                show_alert=True,
            )
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    quality, videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkınızı Arayın.", show_alert=True
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    await CallbackQuery.answer(f"İşleniyor:- {title[:20]}", show_alert=True)
    theme = await check_theme(chat_id)
    chat_title = await specialfont_to_normal(chat_title)
    thumb = await gen_thumb(thumbnail, title, user_id, theme, chat_title)
    nrs, ytlink = await get_m3u8(videoid)
    if nrs == 0:
        return await CallbackQuery.message.reply_text(
            "Video Biçimleri Bulunamadı.."
        )
    await start_live_stream(
        CallbackQuery,
        quality,
        ytlink,
        thumb,
        title,
        duration_min,
        duration_sec,
        videoid,
    )


@app.on_callback_query(filters.regex(pattern=r"VideoStream"))
async def Videos_Stream(_, CallbackQuery):
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    quality, videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkınızı Arayın.", show_alert=True
        )
    if str(duration) == "None":
        buttons = livestream_markup(quality, videoid, duration, user_id)
        return await CallbackQuery.edit_message_text(
            "**Canlı Akış Algılandı**\n\nCanlı yayın oynamak ister misiniz? Bu, geçerli müzik çalmayı durdurur (varsa) ve canlı video akışına başlar.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    if duration_sec > DURATION_LIMIT:
        return await CallbackQuery.message.reply_text(
            f"**Süre Sınırı Aşıldı**\n\n**İzin Verilen Süre: **{DURATION_LIMIT_MIN} dakika(s)\n**Alınan Süre:** {duration_min} dakika(s)"
        )
    await CallbackQuery.answer(f"İşleniyor:- {title[:20]}", show_alert=True)
    theme = await check_theme(chat_id)
    chat_title = await specialfont_to_normal(chat_title)
    thumb = await gen_thumb(thumbnail, title, user_id, theme, chat_title)
    nrs, ytlink = await get_m3u8(videoid)
    if nrs == 0:
        return await CallbackQuery.message.reply_text(
            "Video Biçimleri Bulunamadı.."
        )
    await start_video_stream(
        CallbackQuery,
        quality,
        ytlink,
        thumb,
        title,
        duration_min,
        duration_sec,
        videoid,
    )
