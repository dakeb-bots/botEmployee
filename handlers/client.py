from aiogram.dispatcher import Dispatcher, FSMContext
from create_bot import bot, dp
from aiogram import types
from keyboards import markups
import smtplib
from config import email, email_pass, email_to

from states import states

# SMTP
candidate_dict = []
smtpObject = smtplib.SMTP('smtp.gmail.com', 587)

def send_mail():
    smtpObject.starttls()
    smtpObject.login(email, email_pass)

    fio = f'ФИО: {candidate_dict[0]["fio"]}'
    age = f'Возраст: {candidate_dict[0]["age"]}'
    exp = f'Опыт работы: {candidate_dict[0]["experience"]}'
    phone = f'Телефон: {candidate_dict[0]["phone"]}'

    body = "\r\n".join((f'From {email}',
                       f'To {email_to}',
                       'Subject Новая анкета',
                        fio,
                        age,
                        exp,
                        phone,
                        ''
                        ))
    smtpObject.sendmail(email, email_to, body.encode('utf-8'))
    smtpObject.quit()

async def start(message: types.Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nЧтобы оставить заявку нажмите на кнопку', reply_markup=markups.leave_a_request())

@dp.callback_query_handler(lambda call: call.data)
async def buttons_event(call: types.CallbackQuery):
    if call.data == 'leave_a_request':
        await bot.send_message(call.from_user.id, 'Итак, напишите свою фамилию, имя и отчество')
        await states.FSM_Form.fio.set()
        await bot.answer_callback_query(call.id)

# Анкета
async def load_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
    await states.FSM_Form.next()
    await bot.send_message(message.chat.id, 'Ваш возраст?')

async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await states.FSM_Form.next()
    await bot.send_message(message.chat.id, 'Каков Ваш опыт работы в нашей сфере. Опишите как можно точнее')

async def load_experience(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'] = message.text
    await states.FSM_Form.next()
    await bot.send_message(message.chat.id, 'Введите ваш номер телефона')

async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    candidate_dict.append({'fio': data['fio'],
                           'age': data['age'],
                           'experience': data['experience'],
                           'phone': data['phone']
                           })
    await bot.send_message(message.chat.id, f'Проверим информацию\n' +
                                            f'Имя: {data["fio"]}\n' +
                                            f'Возраст: {data["age"]}\n' +
                                            f'Опыт: {data["experience"]}\n' +
                                            f'Телефон: {data["phone"]}')
    await bot.send_message(message.chat.id, 'Все верно?')
    await states.FSM_Form.next()

async def load_submit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['submit'] = str.lower(message.text)
    if data['submit'] == 'да':
        await bot.send_message(message.chat.id, 'Отлично, мы Вам перезвоним, всего Вам хорошего!')
        # Отправка
        msg = f'Анкета: {data["fio"]}\nФИО: {data["fio"]}\nВозраст: {data["age"]}\nОпыт работы: {data["experience"]}\nТелефон: {data["phone"]}'.encode('utf-8')
        send_mail()
        # Очистка словаря и даты
        candidate_dict = []
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Введите ваше фио')
        candidate_dict = []
        await states.FSM_Form.fio.set()

def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    # FSM
    dp.register_message_handler(load_fio, state=states.FSM_Form.fio)
    dp.register_message_handler(load_age, state=states.FSM_Form.age)
    dp.register_message_handler(load_experience, state=states.FSM_Form.experience)
    dp.register_message_handler(load_phone, state=states.FSM_Form.phone)
    dp.register_message_handler(load_submit, state=states.FSM_Form.submit)
