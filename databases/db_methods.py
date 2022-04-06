import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('db.db')
    cur = base.cursor()
    if base:
        print('Database connected.')
    base.execute()


class SQlite:

    # -------------------- Подключение к бд и сохранение курсора соединения -------------------
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
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
