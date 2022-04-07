import sqlite3 as sq
from create_bot import bot
from keyboards import urlkb


def sql_start():
    global base, cur
    base = sq.connect('databases/db.db')
    cur = base.cursor()
    if base:
        print('Database connected.')


# -------------------------------------- Проверка есть ли юзер в базе
def sql_get_sub(user_id):
    return bool(len(cur.execute("SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()))


# -------------------------------------- Проверка на админа
def sql_is_admin(user_id):
    return cur.execute('SELECT * FROM `subscriptions` WHERE `admin` = 1 AND `user_id` = ?', (user_id,)).fetchall()


# -------------------------------------- Добавить продукт
async def sql_add_product(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO `products` (`name`, `description`, `img`, `price`, `volume`, `composition`, `countInStock`, `category`) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# -------------------------------------- Добавить категорию
async def sql_add_category(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO `category` (`name`) '
                    'VALUES (?)', tuple(data.values()))
        base.commit()


# ------------------------------------- Посмотреть продукт админ
async def sql_view_products_admin(message):
    for product in cur.execute('SELECT * FROM products').fetchall():
        await bot.send_photo(message.from_user.id, product[3], f'id: {product[0]}\n'
                                                               f'Название: {product[1]}\n'
                                                               f'Описание: {product[2]}\n'
                                                               f'Цена: {product[4]}руб.\n'
                                                               f'Объем: {product[5]}мл.\n'
                                                               f'Состав: {product[6]}\n'
                                                               f'Количество на складе: {product[7]}шт.\n'
                                                               f'Категория: {product[8]}', reply_markup=urlkb)


class SQlite:

    # -------------------- Подключение к бд и сохранение курсора соединения -------------------
    def __init__(self, database_file):
        self.connection = sq.connect(database_file)
        self.cursor = self.connection.cursor()

    # -------------------- Получаем всех подписчиков со статусом true ------------------------
    def get_subscriptions(self, status = True):
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
            result = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `admin` = 1 AND `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    # -------------------- Добавление нового подписчика ---------------------------------------
    def add_subscriber(self, user_id, username, first_name, last_name, status=True):
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `username`, `first_name`, `last_name`, `status`) VALUES (?,?,?,?,?)",
                                       (user_id, username, first_name, last_name,  status))

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
