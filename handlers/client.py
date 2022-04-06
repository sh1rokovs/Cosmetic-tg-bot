from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_admin


class FSMAdmin(StatesGroup):
    name = State()
    description = State()
    img = State()
    price = State()
    volume = State()
    composition = State()
    countlnStock = State()
    category = State()


# ------------------------------------ Админ панель --------------------------------
# --------------- Добавить товар
@dp.message_handler(commands='Добавить товар', state=None)
async def add_product_start(message: types.Message):
    await FSMAdmin.name.set()
    await message.reply('Напишите название')


@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введите описание')


@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Пришлите фото товара')


@dp.message_handler(content_types=['photo'], state=FSMAdmin.img)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Укажите цену товара')


@dp.message_handler(state=FSMAdmin.img)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMAdmin.next()
    await message.reply('Напишите состав товара')


# ------------------------------------ Клиентская часть ----------------------------
# ------------------------------------ Общая часть ---------------------------------
@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        if db.is_admin(message.from_user.id):
            await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user) +
                                   '\nДобро пожаловать в "BH cosmetics"', reply_markup=nav.adminMenu)
        else:
            await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user) +
                                   '\nДобро пожаловать в "BH cosmetics"')
    else:
        if db.is_admin(message.from_user.id):
            await bot.send_message(message.from_user.id, 'Приветствую {0.first_name}'.format(message.from_user),
                                   reply_markup=nav.adminMenu)
        else:
            await bot.send_message(message.from_user.id,
                                   "Ждите обновлений")
    print(f'{message.from_user.first_name} start bot: {message.from_user}')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def subscribe(message: types.Message):
    if db.is_admin(message.from_user.id):
        if message.text == "Добавить товар":
            if not db.subscriber_exists(userId):
                db.add_subscriber(message.from_user.id, message.from_user.username,
                                  message.from_user.first_name, message.from_user.last_name)
            else:
                db.update_subscription(userId, True)

            await message.answer("Вы успешно подписались", reply_markup=nav.subMenu)
            print(f'{message.from_user.first_name}: подписался')
    else:
        return


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(hello_message, commands=['start', 'help'])
    dp.register_message_handler(subscribe)
