import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from parsing import get_info_about_meme


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    """Send welcome message"""
    await message.reply("Hello! Give me a GIF and I'll try to find out where it's from.")


@dp.message_handler(content_types='animation')
async def get_gif(message: types.Message) -> None:
    """Send info about the received GIF"""
    # Get file information
    file_id = message.animation.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    # Download the file
    download_path = f'videos/{file_info.file_unique_id}.mp4'
    await bot.download_file(file_path, download_path)

    # Get info about the meme
    info = get_info_about_meme(download_path)
    await message.answer(info)


def run() -> None:
    """Run bot"""
    executor.start_polling(dp, skip_updates=True)
