from core.bot import App
from core import loggers
import sys
import asyncio
# import db
import threading

if __name__ == '__main__':

    if sys.argv[0]:
        try:
            loggers.main.info("Run build telegram bot")
            asyncio.run(App().run())
        except Exception as e:
            print(e)
