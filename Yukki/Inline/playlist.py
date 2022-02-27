from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)


def check_markup(user_name, user_id, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Grubun Çalma Listesi",
                callback_data=f"playlist_check {user_id}|Group|{videoid}",
            ),
            InlineKeyboardButton(
                text=f"{user_name[:8]} Çalma listesi",
                callback_data=f"playlist_check {user_id}|Personal|{videoid}",
            ),
        ],
        [InlineKeyboardButton(text="👉 Menüyü Kapat", callback_data="close")],
    ]
    return buttons


def playlist_markup(user_name, user_id, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Grubun Müzik Listesi",
                callback_data=f"show_genre {user_id}|Group|{videoid}",
            ),
            InlineKeyboardButton(
                text=f"{user_name[:8]} Çalma Listesi",
                callback_data=f"show_genre {user_id}|Personal|{videoid}",
            ),
        ],
        [InlineKeyboardButton(text="👉 Menüyü Kapat", callback_data="close")],
    ]
    return buttons

def play_genre_playlist(user_id, type, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Arabesk",
                callback_data=f"play_playlist {user_id}|{type}|Arabesk",
            ),
            InlineKeyboardButton(
                text=f"Kürtçe",
                callback_data=f"play_playlist {user_id}|{type}|Kürtçe",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Remix",
                callback_data=f"play_playlist {user_id}|{type}|Remix",
            ),
            InlineKeyboardButton(
                text=f"Yabancı",
                callback_data=f"play_playlist {user_id}|{type}|Yabancı",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Dini",
                callback_data=f"play_playlist {user_id}|{type}|Dini",
            ),
            InlineKeyboardButton(
                text=f"Pop",
                callback_data=f"play_playlist {user_id}|{type}|Pop",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Nostaji",
                callback_data=f"play_playlist {user_id}|{type}|Nostaji",
            ),
            InlineKeyboardButton(
                text=f"Karışık",
                callback_data=f"play_playlist {user_id}|{type}|Karışık",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⇦ Geri Dön",
                callback_data=f"main_playlist {videoid}|{type}|{user_id}",
            ),
            InlineKeyboardButton(text="👉 Menüyü Kapat", callback_data="close"),
        ],
    ]
    return buttons


def add_genre_markup(user_id, type, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"✚ Pop",
                callback_data=f"add_playlist {videoid}|{type}|Pop",
            ),
            InlineKeyboardButton(
                text=f"✚ Dini",
                callback_data=f"add_playlist {videoid}|{type}|Dini",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✚ Remix",
                callback_data=f"add_playlist {videoid}|{type}|Remix",
            ),
            InlineKeyboardButton(
                text=f"✚ Yabancı",
                callback_data=f"add_playlist {videoid}|{type}|Yabancı",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✚ Arabesk",
                callback_data=f"add_playlist {videoid}|{type}|Arabesk",
            ),
            InlineKeyboardButton(
                text=f"✚ Kürtçe",
                callback_data=f"add_playlist {videoid}|{type}|Kürtçe",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✚ Nostaji",
                callback_data=f"add_playlist {videoid}|{type}|Nostaji",
            ),
            InlineKeyboardButton(
                text=f"✚ Karışık",
                callback_data=f"add_playlist {videoid}|{type}|Karışık",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⇦ Geri Dön", callback_data=f"goback {videoid}|{user_id}"
            ),
            InlineKeyboardButton(text="👉 Menüyü Kapat", callback_data="close"),
        ],
    ]
    return buttons


def check_genre_markup(type, videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Pop", callback_data=f"check_playlist {type}|Pop"
            ),
            InlineKeyboardButton(
                text=f"Dini", callback_data=f"check_playlist {type}|Dini"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Remix", callback_data=f"check_playlist {type}|Remix"
            ),
            InlineKeyboardButton(
                text=f"Yabancı", callback_data=f"check_playlist {type}|Yabancı"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Arabesk",
                callback_data=f"check_playlist {type}|Arabesk",
            ),
            InlineKeyboardButton(
                text=f"Kürtçe",
                callback_data=f"check_playlist {type}|Kürtçe",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Nostaji",
                callback_data=f"check_playlist {type}|Nostaji",
            ),
            InlineKeyboardButton(
                text=f"Karışık", callback_data=f"check_playlist {type}|Karışık"
            ),
        ],
        [InlineKeyboardButton(text="👉 Menüyü Kapat", callback_data="close")],
    ]
    return buttons


def third_playlist_markup(user_name, user_id, third_name, userid, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Grubun Çalma Listesi",
                callback_data=f"show_genre {user_id}|Group|{videoid}",
            ),
            InlineKeyboardButton(
                text=f"{user_name[:8]}'nin Çalma Listesi",
                callback_data=f"show_genre {user_id}|Personal|{videoid}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{third_name[:16]}'nin Çalma Listesi",
                callback_data=f"show_genre {userid}|third|{videoid}",
            ),
        ],
        [InlineKeyboardButton(text="👉 Kapat", callback_data="close")],
    ]
    return buttons


def paste_queue_markup(url):
    buttons = [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
        [InlineKeyboardButton(text="Sıradaki Çalma Listesi", url=f"{url}")],
        [InlineKeyboardButton(text="👉 Menüyü Kapat", callback_data=f"close")],
    ]
    return buttons


def fetch_playlist(user_name, type, genre, user_id, url):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Oynat {user_name[:10]}'s {genre} Çalma Listesi",
                callback_data=f"play_playlist {user_id}|{type}|{genre}",
            ),
        ],
        [InlineKeyboardButton(text="Çalma listesine Göz At", url=f"{url}")],
        [InlineKeyboardButton(text="👉 Menüyü Kapat", callback_data=f"close")],
    ]
    return buttons


def delete_playlist_markuup(type, genre):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Evet! Sil",
                callback_data=f"delete_playlist {type}|{genre}",
            ),
            InlineKeyboardButton(text="Hayır!", callback_data=f"close"),
        ],
    ]
    return buttons
