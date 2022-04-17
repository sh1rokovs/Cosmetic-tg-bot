import sqlite3 as sq
from create_bot import bot
from keyboards import urlkb


def sql_start():
    global base, cur
    base = sq.connect('databases/db.db')
    cur = base.cursor()
    if base:
        print('Database connected.')


# ////////////////////////////////////////////////////////////////////////////////////////////////////
# -------------------------------------- Проверка есть ли юзер в базе
def sql_get_sub(user_id):
    return bool(len(cur.execute("SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()))


# -------------------------------------- Проверка на админа
def sql_is_admin(user_id):
    return cur.execute('SELECT * FROM `subscriptions` WHERE `admin` = 1 AND `user_id` = ?', (user_id,)).fetchall()


# ------------------------------------- Посмотреть пользователей
async def sql_view_subscriptions(user_id):
    new_subs = ""
    for sub in cur.execute('SELECT * FROM subscriptions').fetchall():
        new_subs += f'login: {sub[2]}\nИмя: {sub[3]}\n---------------\n'
    await bot.send_message(user_id, new_subs)
# ////////////////////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////////
# -------------------------------------- Найти товар по id
def sql_product_id(product_id):
    for product in cur.execute('SELECT * FROM `products` WHERE `id` = ?', (product_id,)).fetchall():
        return [product[3], f'id: {product[0]}\n'
                            f'Название: {product[1]}\n'
                            f'Описание: {product[2]}\n'
                            f'Цена: {product[4]}руб.\n'
                            f'Объем: {product[5]}мл.\n'
                            f'Состав: {product[6]}\n'
                            f'Количество на складе: {product[7]}шт.\n'
                            f'Категория: {product[8]}']


# -------------------------------------- Найти товар по категории
def sql_product_category(product_category):
    product_category = product_category.capitalize()
    for product in cur.execute('SELECT * FROM `products` WHERE `category` = ?', (product_category,)).fetchall():
        return [product[3], f'id: {product[0]}\n'
                            f'Название: {product[1]}\n'
                            f'Описание: {product[2]}\n'
                            f'Цена: {product[4]}руб.\n'
                            f'Объем: {product[5]}мл.\n'
                            f'Состав: {product[6]}\n'
                            f'Количество на складе: {product[7]}шт.\n'
                            f'Категория: {product[8]}']


# -------------------------------------- Добавить продукт
async def sql_add_product(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO `products` (`name`, `description`, `img`, `price`, `volume`, `composition`, `countInStock`, `category`) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# ------------------------------------- Посмотреть продукт админ
async def sql_view_products_admin(user_id):
    for product in cur.execute('SELECT * FROM products').fetchall():
        await bot.send_photo(user_id, product[3], f'id: {product[0]}\n'
                                                  f'Название: {product[1]}\n'
                                                  f'Описание: {product[2]}\n'
                                                  f'Цена: {product[4]}руб.\n'
                                                  f'Объем: {product[5]}мл.\n'
                                                  f'Состав: {product[6]}\n'
                                                  f'Количество на складе: {product[7]}шт.\n'
                                                  f'Категория: {product[8]}', reply_markup=urlkb)
# ////////////////////////////////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////////////////////
# -------------------------------------- Добавить категорию
async def sql_add_category(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO `categories` (`name`) '
                    'VALUES (?)', tuple(data.values()))
        base.commit()


# ------------------------------------- Посмотреть категории
async def sql_view_categories(user_id):
    new_categories = ""
    for category in cur.execute('SELECT * FROM categories').fetchall():
        new_categories += f'Название: {category[1]}\n'
    await bot.send_message(user_id, new_categories)
# /////////////////////////////////////////////////////////////////////////////


class SQlite:

    # -------------------- Подключение к бд и сохранение курсора соединения -------------------
    def __init__(self, database_file):
        self.connection = sq.connect(database_file)
        self.cursor = self.connection.cursor()

    # -------------------- Получаем всех подписчиков со статусом true ------------------------
    def get_subscriptions(self, status=True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    # -------------------- Проверка есть ли юзер в базе ---------------------------------
    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    # -------------------- Проверка на админа ---------------------------------
    def is_admin(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `admin` = 1 AND `user_id` = ?",
                                         (user_id,)).fetchall()
            return bool(len(result))

    # -------------------- Добавление нового подписчика ---------------------------------------
    def add_subscriber(self, user_id, username, first_name, last_name, status=True):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`, `username`, `first_name`, `last_name`, `status`) VALUES (?,?,?,?,?)",
                (user_id, username, first_name, last_name, status))

    # -------------------- Обновляем статус подписки -----------------------------------------
    def update_subscription(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    # -------------------- Проверка есть ли статус у юзера
    def subscribe_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = 1 AND `user_id` = ?",
                                         (user_id,)).fetchall()
            return result

    def close(self):
        self.connection.close()
