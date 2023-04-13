import os
import datetime
import pytz

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
PROXY_URL = "http://proxy.server:3128"
storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'), proxy=PROXY_URL)
dp = Dispatcher(bot=bot, storage=storage)
# keyboards
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Ввести ФИО водителя').add('Инфо').add('Контакт')


def save_user(user_id: int, user_name: str):
    # Формируем строку записи с разделителем
    record = f'{user_id},{user_name}\n'
    # Открываем файл в режиме чтения
    with open('app/user_ids.txt', 'r') as file:
        # Читаем содержимое файла в список строк
        lines = file.readlines()
        # Проверяем, существует ли указанный ID пользователя и его имя в списке строк
        if record not in lines:
            # Если запись отсутствует, то записываем ее в файл
            with open('app/user_ids.txt', 'a') as file:
                file.write(record)
                print(f'ID {user_id} с именем {user_name} успешно добавлен')
        else:
            print(f'Запись с ID {user_id} и именем {user_name} уже существует в файле.')


# abuss
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
        # Добавляем ФИОpytz.timezone('Asia/Yakutsk') водителя на изображение
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/SFProText-Medium.ttf", 40)
        font_time = ImageFont.truetype("fonts/DroidSans.ttf", 40)
        text = message.text
        tz = pytz.timezone('Asia/Yakutsk')
        current_time = datetime.datetime.now(tz)
        time = current_time.strftime("%H:%M")
        # Text
        text_width, text_height = draw.textsize(text, font=font)
        # Time
        text_width1, text_height1 = draw.textsize(time, font=font_time)
        x = 539 - text_width / 2
        y = 700 - text_height / 2
        x1 = 128 - text_width1 / 2
        y1 = 35 - text_height1 / 2
        draw.text((x, y), text, (255, 255, 255), font=font)
        draw.text((x1, y1), time, (255, 255, 255), font=font_time)
        img.save('Images/output.jpg')
        # Отправляем пользователю изображение с ФИО водителя
        with open('Images/output.jpg', 'rb') as photo:
            await bot.send_photo(message.chat.id, photo)
    # Сбрасываем флаг ожидания ФИО водителя для данного пользователя
    context = dp.current_state(chat=message.chat.id)
    await context.reset_state()


# INFO
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


# FIO
@dp.message_handler(text=['Контакт'])
async def cmd_start(message: types.Message):
    await message.answer(f'Разработчик: @powelnahuy00.')


# start!
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await message.answer(f'Приветствую!', reply_markup=main)
    save_user(user_id, username)


if __name__ == '__main__':
    executor.start_polling(dp)
