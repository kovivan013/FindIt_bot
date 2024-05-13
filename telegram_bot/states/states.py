from aiogram.dispatcher.filters.state import State, StatesGroup


class MainMenuStates(StatesGroup):

    welcome = State()
    input_username = State()
    input_description = State()
    input_phone_number = State()
    start_menu = State()


class DashboardStates(StatesGroup):

    select_mode = State()
    input_query = State()
    query_result = State()
    filters = State()
