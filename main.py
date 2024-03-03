import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

logger = logging.getLogger(__name__)


async def main() -> None:

    logging.basicConfig(
        level=logging.DEBUG,
        format="[{asctime}] {levelname:8} {filename}:{lineno} - {name} - {message}",
        style="{",
    )
    
    logger.info("Starting bot")

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
