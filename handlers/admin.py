from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_admin, urlkb
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


class FSMFindCategory(StatesGroup):
    name = State()


class FSMId(StatesGroup):
    id = State()


# --------------- Добавить товар -- готово
async def add_product_start(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await FSMAdmin.name.set()
        await bot.send_message(message.from_user.id, "Введите параметры товара, если параметра нет, ввести 0")
        await message.reply('Напишите название')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введите описание')


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Пришлите фото товара')


async def load_img(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Укажите цену товара')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMAdmin.next()
    await message.reply('Напишите объем упаковки товара')


async def load_volume(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['volume'] = message.text
    await FSMAdmin.next()
    await message.reply('Напишите состав товара')


async def load_composition(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['composition'] = message.text
    await FSMAdmin.next()
    await message.reply('Укажите количество товара на складе')


async def load_countInStock(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['countInStock'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('Укажите категорию')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await db.sql_add_product(state)
    await bot.send_message(message.from_user.id, "Вы успешно добавили товар.")
    await state.finish()


# ----------------- Добавить категорию --- готово
async def product_category(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await FSMCategory.name.set()
        await bot.send_message(message.from_user.id, "Введите название категории:")


async def load_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await db.sql_add_category(state)
    await bot.send_message(message.from_user.id, "Вы успешно добавили категорию.")
    await state.finish()


# ----------------- Посмотреть категории  ---- готово
async def view_categories(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await db.sql_view_categories(message.from_user.id)


# ----------------- Найти по категории -- готово
async def category_name(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await FSMFindCategory.name.set()
        await bot.send_message(message.from_user.id, "Введите название категории:")


async def load_category_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if db.sql_product_category(data['name']):
        await bot.send_photo(message.from_user.id, db.sql_product_category(data['name'])[0],
                             db.sql_product_category(data['name'])[1], reply_markup=urlkb)
    else:
        await bot.send_message(message.from_user.id, 'Товары не найдены')
    await state.finish()


# ----------------- Найти по id -- готово
async def product_id(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await FSMId.id.set()
        await bot.send_message(message.from_user.id, "Введите id товара:")


async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    if db.sql_product_id(int(data['id'])):
        await bot.send_photo(message.from_user.id, db.sql_product_id(int(data['id']))[0],
                             db.sql_product_id(int(data['id']))[1], reply_markup=urlkb)
    else:
        await bot.send_message(message.from_user.id, 'Товар не найден')
    await state.finish()


# ----------------- Посмотреть каталог -- готово
async def view_products(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await db.sql_view_products_admin(message.from_user.id)


# ----------------- Посмотреть подписчиков -- готово
async def view_subs(message: types.Message):
    if db.sql_is_admin(message.from_user.id):
        await db.sql_view_subscriptions(message.from_user.id)


# ------------------ Редактировать товар


# ----------------- Остальное


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(add_product_start, commands=['Добавить_товар'], state=None)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_img, content_types=['photo'], state=FSMAdmin.img)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_volume, state=FSMAdmin.volume)
    dp.register_message_handler(load_composition, state=FSMAdmin.composition)
    dp.register_message_handler(load_countInStock, state=FSMAdmin.countInStock)
    dp.register_message_handler(load_category, state=FSMAdmin.category)
    dp.register_message_handler(product_id, commands=['Найти_по_id'], state=None)
    dp.register_message_handler(load_id, state=FSMId.id)
    dp.register_message_handler(category_name, commands=['Найти_по_категории'], state=None)
    dp.register_message_handler(load_category_name, state=FSMFindCategory.name)
    dp.register_message_handler(product_category, commands=['Добавить_категорию'], state=None)
    dp.register_message_handler(load_product_category, state=FSMCategory.name)
    dp.register_message_handler(view_products, commands=['Каталог'])
    dp.register_message_handler(view_subs, commands=['Посмотреть_пользователей'])
    dp.register_message_handler(view_categories, commands=['Посмотреть_категории'])
