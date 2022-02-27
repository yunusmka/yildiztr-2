import asyncio
import importlib
import os
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytgcalls import idle
from rich.console import Console
from rich.table import Table
from youtubesearchpython import VideosSearch

from config import (LOG_GROUP_ID, LOG_SESSION, STRING1, STRING2, STRING3,
                    STRING4, STRING5)
from Yukki import (ASS_CLI_1, ASS_CLI_2, ASS_CLI_3, ASS_CLI_4, ASS_CLI_5,
                   ASSID1, ASSID2, ASSID3, ASSID4, ASSID5, ASSNAME1, ASSNAME2,
                   ASSNAME3, ASSNAME4, ASSNAME5, BOT_ID, BOT_USERNAME, LOG_CLIENT,
                   OWNER_ID, SUDOERS, app, random_assistant)
from Yukki.Core.Clients.cli import LOG_CLIENT
from Yukki.Core.PyTgCalls.Yukki import (pytgcalls1, pytgcalls2, pytgcalls3,
                                        pytgcalls4, pytgcalls5)
from Yukki.Database import (get_active_chats, get_active_video_chats,
                            get_sudoers, is_on_off, remove_active_chat,
                            remove_active_video_chat)
from Yukki.Inline import private_panel
from Yukki.Plugins import ALL_MODULES
from Yukki.Utilities.inline import paginate_modules

try:
    from config import START_IMG_URL
except:
    START_IMG_URL = None


loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}


async def initiate_bot():
    with console.status(
        "[magenta] Önyükleme Sonlandırılıyor...",
    ) as status:
        ass_count = len(random_assistant)
        if ass_count == 0:
            console.print(
                f"\n[red] Tanımlı Yardımcı İstemci Yok!.. İşlemden Çık"
            )
            return
        try:
            chats = await get_active_video_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_video_chat(chat_id)
        except Exception as e:
            pass
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            pass
        status.update(
            status="[bold blue]Eklentileri Tarama", spinner="earth"
        )
        console.print("Found {} Plugins".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Eklentileri Alma...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "Yukki.Plugins." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f">> [bold cyan]Başarıyla alındı: [green]{all_module}.py"
            )
        console.print("")
        status.update(
            status="[bold blue]Alma Tamamlandı!",
        )
    console.print(
        "[bold green]Tebrikler!! Efsane Music Bot başarıyla başladı!\n"
    )
    try:
        await app.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Music Bot başarıyla başladı!</b>",
        )
    except Exception as e:
        print(
            "\nBot günlük kanalına erişemedi. Botunuzu günlük kanalınıza eklediğinizden ve yönetici olarak yükseltdiğinizden emin olun!"
        )
        console.print(f"\n[red]Bot Durduruluyor")
        return
    a = await app.get_chat_member(LOG_GROUP_ID, BOT_ID)
    if a.status != "administrator":
        print("Logger Kanalında Bot'ı Yönetici Olarak Yükselt")
        console.print(f"\n[red]Stopping Bot")
        return
    console.print(f"\n┌[red] Bot Olarak Başlatıldı {BOT_USERNAME}!")
    console.print(f"├[green] ID :- {BOT_ID}!")
    if STRING1 != "None":
        try:
            await ASS_CLI_1.send_message(
                LOG_GROUP_ID,
                "<b>Tebrikler!! Yardımcı İstemci 1 başarıyla başlatıldı!</b>",
            )
        except Exception as e:
            print(
                "\nYardımcı Hesap 1 günlük Kanalı'na erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve admi olarak tanıttığınızdan emin olunn!"
            )
            console.print(f"\n[red]Bot Durduruluyor")
            return
        try:
            await ASS_CLI_1.join_chat("Sohbetskyfall")
            await ASS_CLI_1.join_chat("Sohbetdestek")
        except:
            pass
        console.print(f"├[red] Asistan 1 Olarak Başladı {ASSNAME1}!")
        console.print(f"├[green] ID :- {ASSID1}!")
    if STRING2 != "None":
        try:
            await ASS_CLI_2.send_message(
                LOG_GROUP_ID,
                "<b>Tebrikler!! Yardımcı İstemci 2 başarıyla başlatıldı!</b>",
            )
        except Exception as e:
            print(
                "\nYardımcı Hesap 2 günlük Kanalı'na erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun!"
            )
            console.print(f"\n[red]Bot Durduruluyor")
            return
        try:
            await ASS_CLI_2.join_chat("Sohbetskyfall")
            await ASS_CLI_2.join_chat("Sohbetdestek")
        except:
            pass
        console.print(f"├[red] Asistan 2 Olarak Başladı {ASSNAME2}!")
        console.print(f"├[green] ID :- {ASSID2}!")
    if STRING3 != "None":
        try:
            await ASS_CLI_3.send_message(
                LOG_GROUP_ID,
                "<b>Tebrikler!! Yardımcı İstemci 3 başarıyla başlatıldı!</b>",
            )
        except Exception as e:
            print(
                "\nYardımcı Hesap 3, Kanal günlüğüne erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun!"
            )
            console.print(f"\n[red]Bot Durduruluyor")
            return
        try:
            await ASS_CLI_3.join_chat("Sohbetskyfall")
            await ASS_CLI_3.join_chat("Sohbetdestek")
        except:
            pass
        console.print(f"├[red] Asistan 3 Olarak Başladı {ASSNAME3}!")
        console.print(f"├[green] ID :- {ASSID3}!")
    if STRING4 != "None":
        try:
            await ASS_CLI_4.send_message(
                LOG_GROUP_ID,
                "<b>Tebrikler!! Yardımcı İstemci 4 başarıyla başlatıldı!</b>",
            )
        except Exception as e:
            print(
                "\nYardımcı Hesap 4 günlük Kanalı'na erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun!"
            )
            console.print(f"\n[red]Bot Durduruluyor")
            return
        try:
            await ASS_CLI_4.join_chat("Sohbetskyfall")
            await ASS_CLI_4.join_chat("Sohbetdestek")
        except:
            pass
        console.print(f"├[red] Asistan 4 Olarak Başladı {ASSNAME4}!")
        console.print(f"├[green] ID :- {ASSID4}!")
    if STRING5 != "None":
        try:
            await ASS_CLI_5.send_message(
                LOG_GROUP_ID,
                "<b>Tebrikler!! Yardımcı İstemci 5 başarıyla başlatıldı!</b>",
            )
        except Exception as e:
            print(
                "\nAssistant Account 5 has failed to access the log Channel. Make sure that you have added your Assistant to your log channel and promoted as admin!"
            )
            console.print(f"\n[red]Bot Durduruluyor")
            return
        try:
            await ASS_CLI_5.join_chat("Sohbetskyfall")
            await ASS_CLI_5.join_chat("Sohbetdestek")
        except:
            pass
        console.print(f"├[red] Asistan 5 Olarak Başladı {ASSNAME5}!")
        console.print(f"├[green] ID :- {ASSID5}!")
    if LOG_SESSION != "None":
        try:
            await LOG_CLIENT.send_message(
                LOG_GROUP_ID,
                "<b>Tebrikler!! Günlükçü İstemcisi başarıyla başlatıldı!</b>",
            )
        except Exception as e:
            print(
                "\nGünlükçü İstemcisi günlük kanalına erişemedi. Logger Hesabınızı günlük kanalınıza eklediğinizden ve yönetici olarak yükseltdiğinizden emin olun!"
            )
            console.print(f"\n[red]Bot Durduruluyor")
            return
        try:
            await LOG_CLIENT.join_chat("Sohbetskyfall")
            await LOG_CLIENT.join_chat("Sohbetdestek")
        except:
            pass
    console.print(f"└[red] Talia Winamp Müzik Botu Önyüklemesi Tamamlandı.")
    if STRING1 != "None":
        await pytgcalls1.start()
    if STRING2 != "None":
        await pytgcalls2.start()
    if STRING3 != "None":
        await pytgcalls3.start()
    if STRING4 != "None":
        await pytgcalls4.start()
    if STRING5 != "None":
        await pytgcalls5.start()
    await idle()
    console.print(f"\n[red]Stopping Bot")


home_text_pm = f"""Merhaba,
Benim adım {BOT_USERNAME}.
Bazı kullanışlı özelliklere sahip bir Telegram Music + Video Akış botu.

Tüm komutlar: / koyarak yazın Örnek-(Example) /oynat gibi..."""


@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message):
    text, keyboard = await help_parser(message.from_user.mention)
    await app.send_message(message.chat.id, text, reply_markup=keyboard)


@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name[0] == "s":
            sudoers = await get_sudoers()
            text = "**__Bot Sudo Kullanıcıları Listesi:-__**\n\n"
            j = 0
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = (
                        user.first_name if not user.mention else user.mention
                    )
                except Exception:
                    continue
                text += f"➤ {user}\n"
                j += 1
            if j == 0:
                await message.reply_text("Sudo Kullanıcısı Yok")
            else:
                await message.reply_text(text)
        if name == "help":
            text, keyboard = await help_parser(message.from_user.mention)
            await message.delete()
            return await app.send_text(
                message.chat.id,
                text,
                reply_markup=keyboard,
            )
        if name[0] == "i":
            m = await message.reply_text("🔎 Bilgi Alınıyor!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍__**Video İzleme Bilgileri**__
❇️**Başlık:** {title}
⏳**Süre:** {duration} Mins
👀**Görüntüleme:** `{views}`
⏰**Yayınlanma Süresi:** {published}
🎥**Kanal ismi:** {channel}
📎**Kanal Bağlantısı:** [Buradan Ziyaret Edin]({channellink})
🔗**Video bağlantısı:** [Link]({link})
⚡️ __Aranıyor Destekleyen {BOT_NAME}t__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Youtube Videosunu İzle", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🔄 Kapat", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
    out = private_panel()
    return await message.reply_text(
        home_text_pm,
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """Merhaba {first_name},
Daha fazla bilgi için butonlara tıklayın.
Tüm komutlar ile kullanılabilir: /
""".format(
            first_name=name
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("shikhar"))
async def shikhar(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@app.on_callback_query(filters.regex("search_helper_mess"))
async def search_helper_mess(_, CallbackQuery):
    await CallbackQuery.message.delete()
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id, text, reply_markup=keyboard
    )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""Merhaba {query.from_user.first_name},

Daha fazla bilgi için düğmelere tıklayın.

Tüm komutlar: /
 """
    if mod_match:
        module = mod_match.group(1)
        if str(module) == "sudousers":
            userid = query.from_user.id
            if userid in SUDOERS:
                pass
            else:
                return await query.answer(
                    "Bu Düğmeye yalnızca SUDO KULLANICILARI tarafından erişilebilir",
                    show_alert=True,
                )
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Geri", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="🔄 Kapat", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    elif home_match:
        out = private_panel()
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
