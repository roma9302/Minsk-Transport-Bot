from aiogram.types import BotCommand

async def default_commands(bot):
    commands = [
        BotCommand(command="start", description="запуск бота"),
        BotCommand(command="search_bus", description="поиск по номеру автобуса"),
        BotCommand(command="search_troll", description="поиск по номеру троллейбуса"),
        BotCommand(command="search_tram", description="поиск по номеру трамвая")
    ]
    await bot.set_my_commands(commands)
