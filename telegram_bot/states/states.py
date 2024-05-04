from aiogram.dispatcher.filters.state import State, StatesGroup


class MainMenuStates(StatesGroup):

    welcome = State()
    input_username = State()
    input_description = State()
    input_phone_number = State()
    start_menu = State()