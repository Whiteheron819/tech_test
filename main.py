import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils import xls_to_sql

load_dotenv()

START_MESSAGE = "Привет! Нажми кнопку, чтобы загрузить xls файл, который передаст данные в базу"
INFO_MESSAGE = (f'Теперь файл можно загрузить. Принимаются только файлы формата xlsx, с тремя заполненными столбцами,' 
                f'в первой строке должны быть имена таблиц: название, URL, xpath запрос')


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


class DownloadFile(StatesGroup):
    file = State()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Загрузить файл"]
    keyboard.add(*buttons)
    await message.answer(
        START_MESSAGE, reply_markup=keyboard
    )


@dp.message_handler(text="Загрузить файл")
async def start_state(message: types.Message):
    await DownloadFile.file.set()
    await message.answer(INFO_MESSAGE)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=DownloadFile.file)
async def download_doc(message: types.Message, state: FSMContext):
    file = await bot.get_file(message.document.file_id)
    await message.document.download()
    await message.answer(xls_to_sql(file.file_path))
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
