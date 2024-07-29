import logging
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
import asyncio
from core.handlers import router
import conf
# import db

from core.ui import ui_text


class App:
    def __init__(self):
        self.bot = Bot(conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
        self.dp = Dispatcher()

    async def run(self):
        try:
            self.dp.include_router(router)
            # await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except Exception as ex:
            logging.exception(ex)

    def get_bot(self):
        return self.bot
