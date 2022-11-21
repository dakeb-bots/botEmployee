from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM_Form(StatesGroup):
    fio = State()
    age = State()
    experience = State()
    phone = State()
    submit = State()

