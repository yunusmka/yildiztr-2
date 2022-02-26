from typing import Dict, List, Union

from Yukki import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        if message.chat.type == "private":
            return await mystic(_, message)
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "Bazı izinlerle yönetici olmalıyım:\n"
                + "\n- **Sesli_Sohbet_Yönetme:** Sesli sohbetleri yönetmek için"
                + "\n- **Mesaj_Silme_Yetkisi:** Bot'un Aranan artıklarını silmek için"
                + "\n- **Baglantı_Yolu_Davet**: Asistanı sohbete davet etmek için."
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli iznim yok."
                + "\n**İzin:** __SESLI SOHBETLERI YÖNETME__"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli iznim yok."
                + "\n**İzin:** __İLETILERİ SİL__"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "I don't have the required permission to perform this action."
                + "\n**İzin:** __KULLANICILARI BAĞLANTIYLA DAVET ETME__"
            )
            return
        return await mystic(_, message)

    return wrapper
