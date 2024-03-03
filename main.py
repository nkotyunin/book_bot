import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import other_handlers, user_handlers

logger = logging.getLogger(__name__)


async def main() -> None:

    logging.basicConfig(
        level=logging.DEBUG,
        format="[{asctime}] {levelname:8} {filename}:{lineno} - {name} - {message}",
        style="{",
    )

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()
    
    logger.info("Starting bot")
    
    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
