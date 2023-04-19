from aiogram import executor
from create_bot import dp
from handlers import client
from utils import sqlite_db


# TODO
# Environment Token
async def on_startup(_):
    print('Bot was successful launched')
    sqlite_db.sql_start()


if __name__ == '__main__':
    client.register_handlers_client(dp)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
