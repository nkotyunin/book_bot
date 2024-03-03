import logging

from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from database.database import users_db, user_data_template
from services.file_handling import book
from keyboards.pagination_kb import create_pagination_keyboard
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


# This handler process the /beggining command and send first page of the book to the user
@router.message(Command(commands="beggining"))
async def process_beggining_command(message: Message):
    users_db[message.from_user.id]["page"] = 1
    await message.answer(
        text=book[1],
        reply_markup=create_pagination_keyboard(
            "backward", f"1/{len(book)}", "forward"
        ),
    )


# This handler process the /continue command and sends the user the page where they left off
@router.message(Command(commands="continue"))
async def process_continue_command(message: Message):
    page_number = users_db[message.from_user.id]["page"]
    await message.answer(
        text=book[page_number],
        reply_markup=create_pagination_keyboard(
            "backward", f"{page_number}/{len(book)}", "forward"
        ),
    )


# Turn page forward
@router.callback_query(F.data == "forward")
async def process_forward_page(callback: CallbackQuery):
    if users_db[callback.from_user.id]["page"] < len(book):
        users_db[callback.from_user.id]["page"] += 1
        await callback.message.edit_text(
            text=book[users_db[callback.from_user.id]["page"]],
            reply_markup=create_pagination_keyboard(
                "backward", 
                f"{users_db[callback.from_user.id]["page"]}/{len(book)}", 
                "forward"
            ),
        )
    await callback.answer()


# Turn page backward
@router.callback_query(F.data == "backward")
async def process_backward_page(callback: CallbackQuery):
    if users_db[callback.from_user.id]["page"] > 1:
        users_db[callback.from_user.id]["page"] -= 1
        await callback.message.edit_text(
            text=book[users_db[callback.from_user.id]["page"]],
            reply_markup=create_pagination_keyboard(
                "backward",
                f"{users_db[callback.from_user.id]["page"]}/{len(book)}",
                "forward"
            )
        )
    await callback.answer()
