from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def leave_a_request():
    btn_lar = InlineKeyboardButton(text='Заполнить анкету', callback_data='leave_a_request')
    markup_leave_a_request = InlineKeyboardMarkup()
    markup_leave_a_request.add(btn_lar)

    return markup_leave_a_request
