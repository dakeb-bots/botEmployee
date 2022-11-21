from aiogram import executor
from create_bot import dp
from datetime import datetime

from handlers import client
client.register_client_handler(dp)

async def on_startup(_):
    print(f'Bot online: {datetime.now()}')

if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=on_startup
                           )
