import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from utils import xls_to_sql

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Загрузить файл"]
    keyboard.add(*buttons)
    await message.answer(
        "Привет! Нажми кнопку, чтобы загрузить xls файл, который передаст данные в базу", reply_markup=keyboard
    )


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_doc(message: types.Message):
    file = await bot.get_file(message.document.file_id)
    await message.document.download()
    await message.answer(xls_to_sql(file.file_path))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
