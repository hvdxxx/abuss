import os
import io

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot = bot, storage = storage)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Ввести ФИО водителя').add('Инфо').add('Контакт')

#abuss
@dp.message_handler(text='Ввести ФИО водителя')
async def start_fio_handler(message: types.Message):
    await message.answer('Жду Имя Отчество Ф. водителя.')
    # Сохраняем флаг ожидания ФИО водителя для данного пользователя
    context = dp.current_state(chat=message.chat.id)
    await context.set_state('waiting_for_fio')

# Вложенный обработчик текстовых сообщений
@dp.message_handler(state='waiting_for_fio')
async def handle_text_messages(message: types.Message):
    with Image.open('Images/Image1.jpg') as img:
        # Добавляем ФИО водителя на изображение
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/SFProText-Medium.ttf", 35)
        draw.text((320, 680), message.text, (255, 255, 255), font=font)
        img.save('Images/output.jpg')
        # Отправляем пользователю изображение с ФИО водителя
        with open('Images/output.jpg', 'rb') as photo:
            await bot.send_photo(message.chat.id, photo)
    # Сбрасываем флаг ожидания ФИО водителя для данного пользователя
    context = dp.current_state(chat=message.chat.id)
    await context.reset_state()


#FIO
@dp.message_handler(text=['Контакт'])
async def cmd_start(message: types.Message):
    await message.answer(f'Разработчик: @powelnahuy00.')

# start!
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Приветствую!', reply_markup=main)

# dont!
#@dp.message_handler()
#async def answer(message: types.Message):
   #await message.reply('Я тебя не понимаю.')

#@dp.errors_handler()
#async def errors_handler(update, error):
    #print(f'Произошла ошибка: {error}')

if __name__ == '__main__':
    executor.start_polling(dp)