from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

register_markup = ReplyKeyboardMarkup(resize_keyboard=True)
register_markup.add(KeyboardButton(text="👤 Ro'yxatdan o'tish"))
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_markup.add(KeyboardButton(text="❎ Bekor Qilish"))

the_registerator_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Yosh Gvardiya", callback_data="Yosh_Gvardiya")],
    [InlineKeyboardButton(text="Yoshlar va Qonun", callback_data="Yoshlar_va_Qonun")],
    [InlineKeyboardButton(text="Shunqorlar", callback_data="Shunqorlar")],
    [InlineKeyboardButton(text="To'maris izdoshlari", callback_data="to'maris")]
])