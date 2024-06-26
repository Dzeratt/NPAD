import os
import asyncio

from Db import dbConnect

from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import *
import aiohttp

from datetime import datetime

import logging

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
router = Router()


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

dbConnect()

kb_user = [
    [types.KeyboardButton(text='РАСХОД'), types.KeyboardButton(text='ДОХОД')]
]
keyboard_user = types.ReplyKeyboardMarkup(keyboard=kb_user, resize_keyboard=True)

kb_currency = [
    [types.KeyboardButton(text='USD'), types.KeyboardButton(text='EUR'), types.KeyboardButton(text='RUB')]
]
keyboard_currency = types.ReplyKeyboardMarkup(keyboard=kb_currency, resize_keyboard=True)

kb_sort = [
    [types.KeyboardButton(text='ПО ВОЗРАСТАНИЮ'), types.KeyboardButton(text='ПО УБЫВАНИЮ')]
]
keyboard_sort = types.ReplyKeyboardMarkup(keyboard=kb_sort, resize_keyboard=True)


conn = dbConnect()


class states(StatesGroup):
    reg_get = State()
    get_amount = State()
    get_date = State()
    save_oper = State()
    get_value = State()
    show = State()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        'Привет, я Oper_Bot.\n'
        'Воспользуйся меню или используй:\n'
        '/reg чтобы зарегистрироваться;\n'
        '/add_operation чтобы добавить операцию;\n'
        '/operations чтобы посмотреть операции'
    )


@router.message(Command('reg'))
async def reg(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    id = message.chat.id
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    if cur.fetchone() is None:
        await state.update_data(id=id)
        await message.answer('Введите логин')
        await state.set_state(states.reg_get)
    else:
        await message.answer('Вы уже зарегистрированы')
        cur.close()
        return


@router.message(states.reg_get)
async def reg_get(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id = data.get('id')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (id, name) VALUES (%s, %s)', (id, message.text))
    conn.commit()
    cur.close()

    await message.answer('Вы успешно зарегистрировались')
    await state.set_state(None)


@router.message(Command('add_operation'))
async def add_operation(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    id = message.chat.id
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    if cur.fetchone() is None:
        await state.update_data(id=id)
        await message.answer('Зарегистрируйтесь')
        cur.close()
        return
    else:
        await message.answer('Какая операция', reply_markup=keyboard_user)
        cur.close()
        await state.set_state(states.get_amount)


@router.message(states.get_amount)
async def get_amount(message: types.Message, state: FSMContext):
    await state.update_data(operation=message.text.lower())
    await message.answer('Введите сумму операции в рублях')
    await state.set_state(states.get_date)


@router.message(states.get_date)
async def get_date(message: types.Message, state: FSMContext):
    sum = message.text

    try:
        float(sum)
    except ValueError:
        await message.answer('Неверное значение')
        return

    sum = float(sum)

    if sum <= 0:
        return

    await state.update_data(amount=sum)

    await message.answer('Введите дату операции (ГГГГ-ММ-ДД)')
    await state.set_state(states.save_oper)


@router.message(states.save_oper)
async def save_oper(message: types.Message, state: FSMContext):
    date = message.text
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        await message.answer('Дата введена неверно')
        return
    date = datetime.strptime(date, '%Y-%m-%d')
    if date >= datetime.now():
        await message.answer('Дата не может быть больше сегодняшней')
        return
    data = await state.get_data()
    amount = data.get('amount')
    operation = data.get('operation')
    cur = conn.cursor()
    cur.execute('INSERT INTO operations (dates, sum, chat_id, type_operations) VALUES (%s, %s, %s, %s)',
                (date, amount, message.chat.id, operation,))
    conn.commit()
    cur.close()

    await message.answer('Операция успешно добавлена')
    await state.set_state(None)


@router.message(Command('operations'))
async def operations(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    id = message.chat.id
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    if cur.fetchone() is None:
        await state.update_data(id=id)
        await message.answer('Зарегистрируйтесь')
        cur.close()
        return
    else:
        await message.answer('Каким методом?', reply_markup=keyboard_sort)
        cur.close()
        await state.set_state(states.get_value)


@router.message(states.get_value)
async def currency(message: types.Message, state: FSMContext):
    await state.update_data(method=message.text)
    await message.answer('В какой валюте?', reply_markup=keyboard_currency)
    await state.set_state(states.show)


@router.message(states.show)
async def show_result(message: types.Message, state: FSMContext):
    value = message.text.strip().upper()
    id = message.chat.id
    cur = conn.cursor()
    data = await state.get_data()
    method = data.get('method')
    if method == 'ПО ВОЗРАСТАНИЮ':
        cur.execute("SELECT * FROM operations WHERE chat_id = '%s' ORDER BY sum ASC", (id,))
    else:
        cur.execute("SELECT * FROM operations WHERE chat_id = '%s' ORDER BY sum DESC", (id,))
    currencies = cur.fetchall()
    if value == 'USD' or value == 'EUR':
        url = 'http://195.58.54.159:8000/rate?currency=' + value
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.json()
        result = ""
        for currency in currencies:
            sum = currency[2]
            result_sum = float(sum) / float(response['rate'])
            result_sum = round(result_sum, 2)
            result += f"Дата: {currency[1]}; Сумма: {result_sum} {value}; Операция: {currency[4]}\n"
        await message.answer(result)
    else:
        result = ''
        for currency in currencies:
            result += f"Дата: {currency[1]}; Сумма: {currency[2]}; Операция: {currency[4]}\n"
        await message.answer(result)
    cur.close()
    await state.set_state(None)


@router.message()
async def anything(message: types.Message, state: FSMContext):
    await message.answer('Такой команды нет. Попробуйте еще раз.')


comands = [
    BotCommand(command='/start', description='Начать работу'),
    BotCommand(command='/reg', description='Регистрация'),
    BotCommand(command='/add_operation', description='Добавить операцию'),
    BotCommand(command='/operations', description='Все операции'),
]


async def main():
    await bot.set_my_commands(comands, scope=BotCommandScopeDefault())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
conn.close()
