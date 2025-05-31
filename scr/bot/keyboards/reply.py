from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚌 Автобусы")],
        [KeyboardButton(text="🚎 Троллейбусы")],
        [KeyboardButton(text="🚊 Трамваи")],
    ],
    resize_keyboard=True
)
