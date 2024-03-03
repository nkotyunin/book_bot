from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.file_handling import book
from lexicon.lexicon import LEXICON


def edit_bookmarks_keyboard(*args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in sorted(args):
        kb_builder.row(
            *[
                InlineKeyboardButton(
                    text=f"{button} - {book[button][:50]}", callback_data=str(button)
                )
            ],
            width=1,
        )

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON["edit_bookmarks_button"], callback_data="edit_bookmarks"
        ),
        InlineKeyboardButton(text=LEXICON["cancel"], callback_data="cancel"),
    )
    
    return kb_builder.as_markup()
