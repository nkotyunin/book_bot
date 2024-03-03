import os
import sys

BOOK_PATH = "book/Bredberi_Marsianskie-hroniki.txt"
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    punctuation = ".,:;!?"
    end = start + page_size
    while text[end:][:1] in punctuation:
        end -= 1
    text = text[start:end]
    text = text[: max(map(text.rfind, punctuation)) + 1]
    return text, len(text)


def prepare_book(path: str) -> None:
    global book, PAGE_SIZE
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    page_number, start = 1, 0
    while start != len(text) - 1:
        part_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        start += page_size
        book[page_number] = part_text
        page_number += 1


prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
