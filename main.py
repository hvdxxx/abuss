import os
import datetime

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot = bot, storage = storage)
current_time = datetime.datetime.now()

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Ввести ФИО водителя').add('Инфо').add('Контакт')

#abuss
@dp.message_handler(text='Ввести ФИО водителя')
async def start_fio_handler(message: types.Message):
    await message.answer('Жду Имя Отчество Ф. водителя.')
    await message.answer('Например: Михаил Петрович А.')
    # Сохраняем флаг ожидания ФИО водителя для данного пользователя
    context = dp.current_state(chat=message.chat.id)
    await context.set_state('waiting_for_fio')

# Вложенный обработчик текстовых сообщений
@dp.message_handler(state='waiting_for_fio')
async def handle_text_messages(message: types.Message):
    with Image.open('Images/Image1.jpg') as img:
        # Добавляем ФИО водителя на изображение
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/SFProText-Medium.ttf", 40)
        font_time = ImageFont.truetype("fonts/DroidSans.ttf", 40)
        text = message.text
        time = current_time.strftime("%H:%M")
        # Text
        text_width, text_height = draw.textsize(text, font=font)
        # Time
        text_width1, text_height1 = draw.textsize(time, font=font_time)
        x = 539 - text_width/2
        y = 700 - text_height/2
        x1 = 128 - text_width1/2
        y1 = 35 - text_height1/2
        draw.text((x, y), text, (255, 255, 255), font=font)
        draw.text((x1, y1), time, (255, 255, 255), font=font_time)
        img.save('Images/output.jpg')
        # Отправляем пользователю изображение с ФИО водителя
        with open('Images/output.jpg', 'rb') as photo:
            await bot.send_photo(message.chat.id, photo)
    # Сбрасываем флаг ожидания ФИО водителя для данного пользователя
    context = dp.current_state(chat=message.chat.id)
    await context.reset_state()


#INFO
@dp.message_handler(text=['Инфо'])
async def cmd_start(message: types.Message):
    await message.answer(f'*Во-первых*, вам надо узнать ФИО водителя автобуса, для этого используется сбербанк '
                         f'или другой банк.\n'
                         f'\n'
                         f'*Во-вторых*, вводите ФИО в формате(внимание!) Имя, Отчество, Ф.\n'
                         f'\n'
                         f'*В-третьих*, показываете водителю полученное изображение и быстро выходите из автобуса.\n'
                         f'\n'
                         f'*Данный телеграм-бот используется на свой страх и риск.*', parse_mode='Markdown')

#FIO
@dp.message_handler(text=['Контакт'])
async def cmd_start(message: types.Message):
    await message.answer(f'Разработчик: @powelnahuy00.')

# start!
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Приветствую!', reply_markup=main)

if __name__ == '__main__':
    executor.start_polling(dp)