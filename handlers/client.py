from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_admin
from databases import db_methods as db


class FSMAdmin(StatesGroup):
    name = State()
    description = State()
    img = State()
    price = State()
    volume = State()
    composition = State()
    countInStock = State()
    category = State()


class FSMCategory(StatesGroup):
    name = State()


# ------------------------------------ Админ панель --------------------------------
# --------------- Добавить товар
async def add_product_start(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await FSMAdmin.name.set()
        await bot.send_message(message.from_user.id, "Введите параметры товара, если параметра нет, ввести 0")
        await message.reply('Напишите название')


async def load_name(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введите описание')


async def load_description(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Пришлите фото товара')


async def load_img(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Укажите цену товара')


async def load_price(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['price'] = message.text
        await FSMAdmin.next()
        await message.reply('Напишите объем упаковки товара')


async def load_volume(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['volume'] = message.text
        await FSMAdmin.next()
        await message.reply('Напишите состав товара')


async def load_composition(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['composition'] = message.text
        await FSMAdmin.next()
        await message.reply('Укажите количество товара на складе')


async def load_countInStock(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['countInStock'] = int(message.text)
        await FSMAdmin.next()
        await message.reply('Укажите категорию')


async def load_category(message: types.Message, state: FSMContext):
    if db.sql_is_admin(message.from_user.id):
        async with state.proxy() as data:
            data['category'] = message.text

        await db.sql_add_product(state)
        await bot.send_message(message.from_user.id, "Вы успешно добавили товар.")
        await state.finish()


# ----------------- Добавить категорию
'''
@dp.message_handler(content_types=types.ContentType.TEXT)
async def subscribe(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        # Каталог
        if message.text == "Добавить категорию":
'''

# ----------------- Остальное
async def other_admin(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        # Каталог
        if message.text == "Каталог":
            await db.sql_view_products_admin(message)


# ------------------------------------ Клиентская часть ----------------------------
# ------------------------------------ Общая часть ---------------------------------
@dp.message_handler(commands=['start'])
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


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(hello_message, commands=['start', 'help'])
    dp.register_message_handler(other_admin, content_types=types.ContentType.TEXT)
    dp.register_message_handler(add_product_start, commands=['Добавить_товар'], state=None)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_img, content_types=['photo'], state=FSMAdmin.img)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_volume, state=FSMAdmin.volume)
    dp.register_message_handler(load_composition, state=FSMAdmin.composition)
    dp.register_message_handler(load_countInStock, state=FSMAdmin.countInStock)
    dp.register_message_handler(load_category, state=FSMAdmin.category)
