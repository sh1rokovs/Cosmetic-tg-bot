from aiogram.utils import executor
from create_bot import dp
from handlers import client
from databases import db_methods


async def on_startup(_):
    print(f'Бот запущен.')
    db_methods.sql_start()


client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
