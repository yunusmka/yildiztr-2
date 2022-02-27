import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import LOG_SESSION, OWNER_ID
from Yukki import (ASSISTANT_PREFIX, BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME,
                   OWNER_ID, SUDOERS, app)
from Yukki.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo,
                            set_video_limit)

__MODULE__ = "SudoUsers"
__HELP__ = f"""

**<u>SUDO KULLANICILARI EKLEME VE KALDIRMA :</u>**
/addsudo [Kullanıcı adı veya Kullanıcıya yanıt verin]
/delsudo [Kullanıcı adı veya Kullanıcıya yanıt verin]

**<u>HEROKU:</u>**
/get_log - Heroku'dan son 100 satırın günlüğü.
/usage - Dyno Kullanımı.

**<u>YAPILANDIRMA:</u>**
/get_var - Heroku veya .env'den yapılandırma var'ı alma.
/del_var - Heroku veya .env üzerindeki herhangi bir var'ı silme.
/set_var [Var Adı] [Değer] - Heroku veya .env üzerinde bir Var ayarlayın veya Var Güncelleştirin. Var'ı ve Değerini bir boşlukla ayırma.

**<u>BOT COMMANDS:</u>**
/restart - Botu Yeniden Başlat. 
/update - Bot'ı Güncelleştir.
/clean - Temp Dosyalarını Temizle .
/maintenance [enable / disable] 
/logger [enable / disable] - Bot, aranan sorguları günlükçü grubunda günlüğe kaydeder.

**<u>İSTATİSTİK KOMUTLARI:</u>**
/activevc - Botta etkin sesli sohbetleri kontrol edin.
/activevideo - Botta etkin görüntülü aramaları denetleme.
/stats - Bot istatistiklerini kontrol edin

**<u>KARA LİSTE SOHBET İŞLEVİ:</u>**
/blacklistchat [CHAT_ID] - Music Bot kullanarak herhangi bir sohbeti kara listeye alma
/whitelistchat [CHAT_ID] - Music Bot'un kullanılmasından kara listeye alınan herhangi bir sohbeti beyaz listeye alma

**<u>REKLAM İŞLEVİ:</u>**
/broadcast [İleti veya İletiyi Yanıtlama] - Bot'un Sunulan Sohbetlerine herhangi bir mesaj yayınla.
/broadcast_pin [İleti veya İletiyi Yanıtlama] - Bot'un Sunulan Sohbetlerine herhangi bir mesaj yayınla ve mesaj sohbete sabitlenir [Disabled Bildirim].
/broadcast_pin_loud [İleti veya İletiyi Yanıtlama] - Bot'un Sunulan Sohbetlerine herhangi bir mesaj yayınla ve mesaj sohbete sabitlenir [Enabled Bildirim].

**<u>GBAN İŞLEVİ:</u>**
/gban [Kullanıcı adı veya Kullanıcıya yanıt verme] - Bot'un Sunulan Sohbetleri'nde bir kullanıcıyı genel olarak yasaklama ve kullanıcının bot komutlarını kullanmasını engelleme.
/ungban [Kullanıcı adı veya Kullanıcıya yanıt verme] - Kullanıcıyı Bot'un GBan Listesinden kaldırma.

**<u>ASSİSTANT KATIL AYRIL İŞLEVİ:</u>**
/joinassistant [Sohbet Kullanıcı Adı veya Sohbet Kimliği] - Gruba yardımcı katılma.
/leaveassistant [Sohbet Kullanıcı Adı veya Sohbet Kimliği] - Asistan belirli bir gruptan ayrılacak.
/leavebot [Sohbet Kullanıcı Adı veya Sohbet Kimliği] - Bot belirli bir sohbeti terk edecek.

**<u>VIDEOCALLS İŞLEVİ:</u>**
/set_video_limit [Sohbet Sayısı] - Görüntülü Aramalar için aynı anda izin verilen maksimum Sohbet Sayısını ayarlama.

**<u>YARDIMCI İŞLEVİ:</u>**
{ASSISTANT_PREFIX[0]}block [Kullanıcı İletisini Yanıtlama] - Kullanıcıyı Asistan Hesabından Engeller.
{ASSISTANT_PREFIX[0]}unblock [Kullanıcı İletisini Yanıtlama] - Kullanıcının Asistan Hesabıyla Olan Engelini Kaldırır.
{ASSISTANT_PREFIX[0]}approve [Kullanıcı İletisini Yanıtlama] - Kullanıcıyı DM için Onaylar.
{ASSISTANT_PREFIX[0]}disapprove [Kullanıcı İletisini Yanıtlama] - Kullanıcıyı DM için onaylar.
{ASSISTANT_PREFIX[0]}pfp [Fotoğrafı Yanıtlama] - Yardımcı hesap PFP'sini değiştirir.
{ASSISTANT_PREFIX[0]}bio [Biyo metin] - Asistan Hesabının Biyografisini Değiştirir.
"""
# Sudo Kullanıcıları Ekle!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Kullanıcının iletisini yanıtlama veya kullanıcı adı verme/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                f"{user.mention} zaten bir SUDO kullanıcısı."
            )
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"Eklendi **{user.mention}** Sudo Kullanıcılarına."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        else:
            await message.reply_text("Başarısız")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"{message.reply_to_message.from_user.mention} zaten bir SUDO kullanıcısı."
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            f"Eklendi **{message.reply_to_message.from_user.mention}** Sudo Kullanıcılarına"
        )
        os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("Başarısız")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Kullanıcının iletisini yanıtlama veya kullanıcı adı verme/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id not in SUDOERS:
            return await message.reply_text(f"Bot'un Sudo'sunun bir parçası değil.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(
                f"Kaldırıldı **{user.mention}** Kaynak {MUSIC_BOT_NAME}'s Sudo."
            )
            return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        await message.reply_text(f"Yanlış bir şey oldu.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in SUDOERS:
        return await message.reply_text(
            f"Bir parçası değil {MUSIC_BOT_NAME}'s Sudo."
        )
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(
            f"Kaldırıldı **{mention}** Kaynak {MUSIC_BOT_NAME}'s Sudo."
        )
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    await message.reply_text(f"Yanlış bir şey oldu..")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "⭐️<u> **Sahipler:**</u>\n"
    sex = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            sex += 1
        except Exception:
            continue
        text += f"{sex}➤ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n⭐️<u> **Sudo Kullanıcıları:**</u>\n"
                sex += 1
                text += f"{sex}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("Sudo Kullanıcısı Yok")
    else:
        await message.reply_text(text)


### Video Sınırı


@app.on_message(
    filters.command(["set_video_limit", f"set_video_limit@{BOT_USERNAME}"])
    & filters.user(SUDOERS)
)
async def set_video_limit_kid(_, message: Message):
    if len(message.command) != 2:
        usage = "**Kullanım:**\n/set_video_limit [İzin verilen sohbet sayısı]"
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    try:
        limit = int(state)
    except:
        return await message.reply_text(
            "Sınırı Ayarlamak İçin Lütfen Sayısal Sayılar Kullanın."
        )
    await set_video_limit(141414, limit)
    await message.reply_text(
        f"Video Aramaları En Fazla Tanımlı Sınırı {limit} Sohbet."
    )


## Bakım Efsane Music


@app.on_message(filters.command("maintenance") & filters.user(SUDOERS))
async def maintenance(_, message):
    usage = "**Kullanım:**\n/maintenance [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("Bakım için Etkinleştirildi")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("Bakım Modu Devre Dışı")
    else:
        await message.reply_text(usage)


## Günlükçü


@app.on_message(filters.command("logger") & filters.user(SUDOERS))
async def logger(_, message):
    if LOG_SESSION == "None":
        return await message.reply_text(
            "Günlükçü Hesabı Tanımlanmadı.\n\nLütfen Ayarlayın <code>LOG_SESSION</code> var ve sonra günlüğe kaydetmeyi deneyin."
        )
    usage = "**Kullanım:**\n/logger [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 5
        await add_on(user_id)
        await message.reply_text("Etkin Günlüğe Kaydetme")
    elif state == "disable":
        user_id = 5
        await add_off(user_id)
        await message.reply_text("Günlüğe Kaydetme Devre Dışı")
    else:
        await message.reply_text(usage)


## Gban Module


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**Usage:**\n/gban [USERNAME | USER_ID]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "Kendini gban mı istiyorsun? Ne Kadar Aptalca!"
            )
        elif user.id == BOT_ID:
            await message.reply_text("Kendimi engellemeli miyim? Şakamısın abi!")
        elif user.id in SUDOERS:
            await message.reply_text("Sudo kullanıcısını engellemek mi istiyorsunuz? Baksen")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Küresel Yasaklama Başlat {user.mention}**\n\nBeklenen Süre : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Yeni Küresel Yasak {MUSIC_BOT_NAME}**__

**Köken:** {message.chat.title} [`{message.chat.id}`]
**Sudo Kullanıcısı:** {from_user.mention}
**Yasaklı Kullanıcı:** {user.mention}
**Yasaklanmış Kullanıcı Kimliği:** `{user.id}`
**Sohbet:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Kendini engellemek mi istiyorsun? Ne Kadar Aptalca!")
    elif user_id == BOT_ID:
        await message.reply_text("Kendimi engellemeli miyim?? Kim dedi ya!")
    elif user_id in sudoers:
        await message.reply_text("Sudo kullanıcısını engellemek istiyorsunuz? Hadi camım sende")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("Zaten Gbanned.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Gobal Yasağını Başlatmak {mention}**\n\nBeklenen Süre : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Yeni Küresel Yasak {MUSIC_BOT_NAME}**__

**Köken:** {message.chat.title} [`{message.chat.id}`]
**Sudo Kullanıcısı:** {from_user_mention}
**Yasaklı Kullanıcı:** {mention}
**Yasaklanmış Kullanıcı Kimliği:** `{user_id}`
**Sohbet:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**Kullanım:**\n/ungban [USERNAME | USER_ID]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("Engelini kaldırmak istiyorsun.?")
        elif user.id == BOT_ID:
            await message.reply_text("Engelimi kaldırmalı mıyım??")
        elif user.id in sudoers:
            await message.reply_text("Sudo kullanıcıları olamaz blocked/unblocked.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("O zaten özgür, neden ona zorbalık etti?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Ungbanned!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Engelini kaldırmak istiyorsun.?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Engelimi kaldırmalı mıyım? Ama engellenmedim.."
        )
    elif user_id in sudoers:
        await message.reply_text("Sudo kullanıcıları olamaz, blocked/unblocked.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("O zaten özgür, neden ona zorbalık etti?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Ungbanned!")


# Yayın İletisi (Reklam) 


@app.on_message(filters.command("broadcast_pin") & filters.user(SUDOERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Yayınlanan İleti {sent}  Sohbetler {pin} Pins.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/broadcast [MESSAGE] veya [Mesaj'a yanıt verme]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Yayınlanan İleti {sent} Sohbetler ve {pin} Pins.**"
    )


@app.on_message(filters.command("broadcast_pin_loud") & filters.user(SUDOERS))
async def broadcast_message_pin_loud(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Yayınlanan İleti {sent}  Sohbetler {pin} Pins.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/broadcast [MESSAGE] veya [İletiyi Yanıtlama]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Yayınlanan İleti {sent} Sohbetler ve {pin} Pins.**"
    )


@app.on_message(filters.command("reklam") & filters.user(SUDOERS))
async def reklam(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**Yayınlanan İleti {sent} Sohbet.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/reklam [MESSAGE] veya [İletiyi Yanıtla]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**Yayınlanan İleti {sent} Sohbet.**")


# Clean


@app.on_message(filters.command("clean") & filters.user(SUDOERS))
async def clean(_, message):
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("Tümü başarıyla temizlendi **temp** dir(s)!")
