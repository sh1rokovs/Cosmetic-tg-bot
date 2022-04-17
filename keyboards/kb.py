from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton('/Добавить_товар')
b2 = KeyboardButton('/Удалить_товар')
b3 = KeyboardButton('/Каталог')
b4 = KeyboardButton('/Найти_по_id')
b5 = KeyboardButton('/Найти_по_категории')
b6 = KeyboardButton('/Посмотреть_пользователей')
b7 = KeyboardButton('/Добавить_категорию')
b8 = KeyboardButton('/Посмотреть_категории')
b9 = KeyboardButton('/Редактировать_товар')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(b1, b2).row(b7, b8).row(b3, b4, b5).row(b9).row(b6)

urlkb = InlineKeyboardMarkup(row_width=1)
urlMe = InlineKeyboardButton(text='Заказать', url='https://t.me/')
urlkb.add(urlMe)
