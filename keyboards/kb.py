from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Добавить товар')
b2 = KeyboardButton('Удалить товар')
b3 = KeyboardButton('Посмотреть пользователей')

kb_admin = ReplyKeyboardMarkup()

kb_admin.add(b1).add(b2).add(b3)
