from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton('/Добавить_товар')
b2 = KeyboardButton('/Удалить_товар')
b3 = KeyboardButton('Каталог')
b4 = KeyboardButton('/Посмотреть_пользователей')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b1, b2, b3, b4)

urlkb = InlineKeyboardMarkup(row_width=1)
urlMe = InlineKeyboardButton(text='Заказать', url='///')
urlkb.add(urlMe)
