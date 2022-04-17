from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_admin
from databases import db_methods as db


# ------------------------------------ Общая часть ---------------------------------
async def hello_message(message: types.Message):
    if not db.sql_get_sub(message.from_user.id):
        if db.sql_is_admin(message.from_user.id):
            await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user) +
                                   '\nДобро пожаловать в "BH cosmetics"'
                                   '', reply_markup=kb_admin)
        else:
            await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user) +
                                   '\nДобро пожаловать в "BH cosmetics"'
                                   '\nОткрытие позже')
    else:
        if db.sql_is_admin(message.from_user.id):
            await bot.send_message(message.from_user.id, 'Приветствую {0.first_name}'.format(message.from_user),
                                   reply_markup=kb_admin)
        else:
            await bot.send_message(message.from_user.id,
                                   "Открытие позже")
    print(f'{message.from_user.first_name} start bot: {message.from_user}')


def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(hello_message, commands=['start', 'help'])
