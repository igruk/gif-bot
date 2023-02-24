from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import shutil
import asyncio
import motor.motor_asyncio
from images import *
from searching_parsing import *


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
db = client.gif_bot_db
collection = db.gif_bot

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    '''зберігаємо інформацію про користувача в базі даних і пишемо повідомлення'''

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    user = await collection.find_one({'user_id': user_id})

    if user is not None:
        await message.answer("Welcome back!")
        return

    await collection.insert_one({"user_id": user_id, "username": username, "first_name": first_name, "last_name": last_name})

    await message.reply("Hello! Give me a GIF and I'll try to find out where it's from.")


@dp.message_handler(content_types='animation')
async def get_gif(message: types.Message):
    '''отримуємо гіфку і повертаємо результат'''

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    try:
        src = 'downloads/' + message.document.file_name
    except:
        src = 'downloads/' + message.document.file_unique_id + '.mp4'
    await bot.download_file(file_path, src)

    list_frames = get_frames(src[10:])

    for i in range(len(list_frames)):
        frame = list_frames[i]
        result = get_result(frame)
        query = get_query(result)
        if i == 0:
            q = query[0].title()
        try:
            meme_urls = get_knowyourmeme_url(query)
            for meme_url in meme_urls:
                if valid_meme(meme_url, list_frames):
                    info_about_gif = get_info_about_meme(meme_url)
                    return await message.answer(info_about_gif)
        except Exception as error:
            print(error)

    try:
        shutil.rmtree('downloads/')
    except Exception as error:
        print(error)

    info_about_gif = q

    return await message.answer(info_about_gif)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)