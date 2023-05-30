from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterStates(StatesGroup):
    full_name = State()
    passport = State()
    age = State()
    event = State()
    address = State()
    photo = State()
    phone_number = State()
    confirm = State()