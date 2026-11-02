from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from state import router as state_router
from callback import router as callback_router
from connection import *
from keybord import *
from service import *
import os
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()




@dp.message(Command("start"))
async def start_bot(message: Message):
    if await get_user_by_id(message.from_user.id):
        status = await check_admin(message.from_user.id)
        if status:
            await message.answer(f"Welcome Admin! @{message.from_user.username}",reply_markup=admin_key)
        else:
            await message.answer(f"Welcome back! @{message.from_user.username}",reply_markup=users_key)
    else:
        user = message.from_user
        await create_user(user.username,user.full_name,user.id)
        await message.answer(f"Welcome! @{message.from_user.username}",reply_markup=users_key)



@dp.message(Command("help"))
async def help_bot(message: Message):
    await message.answer(f"""
Music Playlist Bot


/start - Start the bot
/add_song - Add a new song
/songs - Show all songs
/playlist - Show your playlist
/playlist_stats - Show playlist statistics
/cancel - Cancel current action
""")

async def main():
    await create_table()
    print("Bot started")
    dp.include_router(state_router)
    dp.include_router(callback_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())