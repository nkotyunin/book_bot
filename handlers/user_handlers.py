import logging

from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database.database import users_db, user_data_template
from lexicon.lexicon import LEXICON

logger = logging.getLogger(__name__)

router = Router()


# This handler will be triggered by the START COMMAND
@router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(text=LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_data_template)
        logger.info(f"User ID {message.from_user.id} has been added to the database")


# This handler will be triggered by the HELP COMMAND
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(text=LEXICON[message.text])
