from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_kb
from config import ADMINS
import uuid

print(uuid.uuid1())
gen_id=uuid.uuid1()
class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    direction = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id not in ADMINS:
        print()
    elif message.chat.type == 'private':
        await FSMAdmin.name.set()
        await message.answer("Как звать?", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Пиши в личке!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = gen_id
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Скока лет?")


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пиши числа")
    elif int(message.text) < 5 or int(message.text) > 50:
        await message.answer("Возростное ограничение!")
    else:
        async with state.proxy() as data:
            data['age'] = int(message.text)
        await FSMAdmin.next()
        await message.answer("Направление? ")


async def load_direc(message: types.Message, state: FSMContext):
    if message.text not in ["Backand", "Android", "UXUI", "Другое"]:
        await message.answer("Выбери из списка!")
    else:
        async with state.proxy() as data:
            data['direction'] = message.text
        await FSMAdmin.next()
        await message.answer("Группа?? Пример:24 1", reply_markup=client_kb.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Числа!!!")
    else:
        async with state.proxy() as data:
            data['group'] = message.text
        await FSMAdmin.next()
        await message.answer("Все верно?", reply_markup=client_kb.submit_markup)





async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        # Запись в БД
        await state.finish()
        await message.answer("Ты зареган")
    elif message.text.lower() == "нет":
        await state.finish()
        await message.answer("Ну и пошел ты!")
    else:
        await message.answer('НИПОНЯЛ!?')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Ну и пошел ты!")


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_fsm, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_direc, state=FSMAdmin.direction)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)