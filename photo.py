import os
import io

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)
fon = ImageFont.truetype('arial.ttf', size=36)

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

@dp.message_handler(commands=['photo'])
async def send_photo(message: types.Message):
    with Image.open('Images/Image.jpg') as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)  # выбираем шрифт и его размер
        draw.text((50, 50), "EBAAAAAAAAAAA!", (255, 255, 255), font=font)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        await bot.send_photo(message.chat.id, img_buffer)

if __name__ == '__main__':
    executor.start_polling(dp)