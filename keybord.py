from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import *


users_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Songs"), KeyboardButton(text="My playlist")],
        [KeyboardButton(text="Help")]],
    resize_keyboard=True
)


admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add song"), KeyboardButton(text="Delete song")],
        [KeyboardButton(text="Songs")],
        [KeyboardButton(text="My playlist"), KeyboardButton(text="Help")]],
    resize_keyboard=True
)



def song_buttons(song_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Listen", callback_data=f"listen_{song_id}"),
            InlineKeyboardButton(text="Add to playlist", callback_data=f"add_{song_id}")]]
    )


def playlist_buttons(song_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Listen", callback_data=f"listen_{song_id}"),
            InlineKeyboardButton(text="Remove from playlist", callback_data=f"remove_{song_id}")]]
    )


def delete_song_buttons(song_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Delete",callback_data=f"delete_{song_id}")]]
    )