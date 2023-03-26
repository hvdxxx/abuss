import os
import io

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Ввести ФИО водителя').add('Инфо').add('Контакт')

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo_photo(message: types.Message):
    # загружаем изображение из файла
    await message.answer(f'Отправлено2.')
    with Image.open('Images/Image.jpg') as img:
        # добавляем текст на изображение
        user_text = message.text
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 50)  # выбираем шрифт и его размер
        draw.text((50, 50), user_text, (255, 255, 255), font=font)  # добавляем текст на изображение
        img.save('Images/output.jpg')  # сохраняем изображение с текстом
        # отправляем пользователю изображение с текстом
        with open('Images/output.jpg', 'rb') as photo:
            await bot.send_photo(message.chat.id, photo)
            await message.answer(f'Отправлено2.')

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
#@dp.message_handler()
#async def answer(message: types.Message):
   #await message.reply('Я тебя не понимаю.')

#@dp.errors_handler()
#async def errors_handler(update, error):
    #print(f'Произошла ошибка: {error}')

if __name__ == '__main__':
    executor.start_polling(dp)