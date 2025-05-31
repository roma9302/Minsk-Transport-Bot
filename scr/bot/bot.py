from aiogram import Bot, Dispatcher
import asyncio
from config.settings import TOKEN
from scr.bot.handlers import search_routes, start
from scr.bot.keyboards.commands import default_commands
from scr.bot.handlers import search_stops 
from scr.bot.handlers import search_times
from scr.bot.handlers import back_handler
from scr.bot.handlers import reply
import logging


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    dp.include_router(start.router)

    dp.include_router(search_routes.router)
    
    dp.include_router(search_stops.router)
    
    dp.include_router(search_times.router)
    
    dp.include_router(back_handler.router)
    
    dp.include_router(reply.router)
        
    await default_commands(bot)

    await dp.start_polling(bot)
    
    logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    asyncio.run(main())
