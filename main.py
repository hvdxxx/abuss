import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Ввести ФИО водителя').add('Инфо').add('Контакт')

#abuss
@dp.message_handler(text=['Ввести ФИО водителя'])
async def cmd_start(message: types.Message):
    await message.answer(f'Жду ФИО водителя.')

#FIO
@dp.message_handler(text=['Контакт'])
async def cmd_start(message: types.Message):
    await message.answer(f'Разработчик: @powelnahuy00.')

# start!
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Приветствую!', reply_markup=main)

# dont!
@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')

if __name__ == '__main__':
    executor.start_polling(dp)