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


class GetAnnouncementStates(StatesGroup):

    preview = State()


class AddAnnouncementStates(StatesGroup):

    select_mode = State()
    input_title = State()
    input_description = State()
    input_photo = State()
    input_location = State()
    input_date = State()
    input_tags = State()
    secret_question = State()
    encrypted_answer = State()


