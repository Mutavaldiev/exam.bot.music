from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from service import *
from keybord import *
from aiogram.types import CallbackQuery


router = Router()


class AddSong(StatesGroup):
    get_title = State()
    get_artist = State()
    get_audio = State()


@router.message(F.text == "Add song")
@router.message(Command("add_song"))
async def add_song(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await state.clear()
        await message.answer("Enter the song title:")
        await state.set_state(AddSong.get_title)
    else:
        await message.answer("Only admin can add songs!")
        await state.clear()




@router.message(AddSong.get_title)
async def get_title_song(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Enter the artist name:")
    await state.set_state(AddSong.get_artist)




@router.message(AddSong.get_artist)
async def get_artist_song(message: Message, state: FSMContext):
    await state.update_data(artist=message.text)
    await message.answer("Send the audio file:")
    await state.set_state(AddSong.get_audio)




@router.message(AddSong.get_audio)
async def get_audio_song(message: Message, state: FSMContext):
    if not message.audio:
        await message.answer("Please send an audio file")
        return
    audio = message.audio
    await state.update_data(audio_file_id=audio.file_id)
    data = await state.get_data()
    author_id = str(message.from_user.id)
    if await add_song_db(data["title"],data["artist"],data["audio_file_id"],author_id):
        await message.answer("Song added successfully!")
    else:
        await message.answer("An error adding the song")
    await state.clear()




@router.message(Command("cancel"))
async def cancel_add_song(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Song adding process cancelled")



@router.message(F.text == "Songs")
@router.message(Command("songs"))
async def show_songs(message: Message):
    songs = await get_all_songs()
    if not songs:
        await message.answer("No songs found.")
        return
    for song in songs:
        await message.answer(f"{song["title"]} - {song["artist"]}",reply_markup=song_buttons(song["songs_id"]))




@router.message(F.text == "My playlist")
@router.message(Command("playlist"))
async def show_playlist(message: Message):
    songs = await get_user_playlist(message.from_user.id)
    if not songs:
        await message.answer("Your playlist is empty.")
        return
    for song in songs:
        await message.answer( f"{song["title"]} - {song["artist"]}", reply_markup=playlist_buttons(song["songs_id"]))





@router.message(Command("playlist_stats"))
async def playlist_stats(message: Message):
    count = await get_playlist_stats(message.from_user.id)
    await message.answer(f"Your playlist contains {count} songs.")





@router.message(F.text == "Delete song")
async def delete_song_handler(message: Message):
    if await check_admin(message.from_user.id):
        songs = await get_all_songs()
        if not songs:
            await message.answer("No songs found!")
            return
        for song in songs:
            await message.answer(f"{song["title"]} - {song["artist"]}",reply_markup=delete_song_buttons(song["songs_id"]))
    else:
        await message.answer("Only admin can delete songs!")