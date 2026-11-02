from aiogram import Router, F
from service import *
from keybord import *
from aiogram.types import CallbackQuery


router = Router()



@router.callback_query(F.data.startswith("listen_"))
async def listen_song(callback: CallbackQuery):
    try:
        song_id = int(callback.data.split("_")[1])
        song = await get_song_by_id(song_id)
        if not song:
            await callback.answer("Song not found", show_alert=True)
            return
        await callback.message.answer_audio(audio=song["audio_file_id"],caption=f'{song["title"]} - {song["artist"]}')
        await callback.answer()
    except ValueError as Error:
        await callback.answer(f"Invalid callback data {Error}")





@router.callback_query(F.data.startswith("add_"))
async def add_to_playlist(callback: CallbackQuery):
    try:
        song_id = int(callback.data.split("_")[1])
        result = await add_song_to_playlist(callback.from_user.id, song_id)
        if result:
            await callback.answer("Added to playlist!")
        else:
            await callback.answer("Could not add song", show_alert=True)
    except ValueError as Error:
        await callback.answer(f"Invalid callback data {Error}")





@router.callback_query(F.data.startswith("remove_"))
async def remove_from_playlist(callback: CallbackQuery):
    try:
        song_id = int(callback.data.split("_")[1])
        result = await remove_song_from_playlist(callback.from_user.id, song_id)
        if result:
            await callback.answer("Removed from playlist!")
        else:
            await callback.answer("Song not found in playlist", show_alert=True)
    except ValueError as Error:
        await callback.answer(f"Invalid callback data {Error}")





@router.callback_query(F.data.startswith("delete_"))
async def delete_song_callback(callback: CallbackQuery):
    if await check_admin(callback.from_user.id):
        song_id = int(callback.data.split("_")[1])
        if await delete_song(song_id):
            await callback.message.edit_text("Music deleted succesfuly! ✅")
            await callback.answer()
        else:
            await callback.answer("Error", show_alert=True)
    else:
        await callback.answer("Only admin can delete songs!", show_alert=True)