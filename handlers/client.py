import datetime
import utils.parser_schedule as ps
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards import kb_client
from utils import sqlite_db


async def command_start(msg: types.message):
    await msg.answer("Привет, я бот который отправляю расписание пар Колледжа связи", reply_markup=kb_client)


async def command_schedule_week(msg: types.message):
    group_name = await sqlite_db.get_group_name(msg.chat.id)
    url = ps.get_link_schedule_group(group_name)
    if url is None:
        await msg.answer(f'Группы: {group_name} не существует')
        return
    lessons = ps.get_lessons_week(url)

    answer = f'🗓 Расписание на неделю\n'
    for i in lessons:
        answer += f'Дата:{i.date}\n'
        answer += f'Номер:{i.number}\n'
        answer += f'Время:{i.time}\n'
        answer += f'Тип:{i.way}\n'
        answer += f'Пара:{i.content}\n'
        answer += f'-------\n'
    await msg.answer(answer)


async def command_schedule_tomorrow(msg: types.message):
    group_name = await sqlite_db.get_group_name(msg.chat.id)
    url = ps.get_link_schedule_group(group_name)
    if url is None:
        await msg.answer(f'Группы: {group_name} не существует')
        return
    lessons = ps.get_lessons(url)
    today = datetime.date.today()
    tomorrow = (today + datetime.timedelta(days=1)).strftime('%d.%m.%Y')

    answer = f'🗓 Расписание на завтра: \n'
    for i in lessons:
        if i.date == tomorrow:
            answer += (f'Дата:{i.date}\n')
            answer += (f'Номер:{i.number}\n')
            answer += (f'Время:{i.time}\n')
            answer += (f'Тип:{i.way}\n')
            answer += (f'Пара:{i.content}\n')
            answer += (f'--------\n')
    if answer == f'🗓 Расписание на завтра: \n':
        answer += f'Завтра нету пар'
    await msg.answer(answer)


async def command_schedule_today(msg: types.message):
    group_name = await sqlite_db.get_group_name(msg.chat.id)
    url = ps.get_link_schedule_group(group_name)
    if url is None:
        await msg.answer(f'Группы: {group_name} не существует')
        return
    lessons = ps.get_lessons(url)
    today = datetime.date.today()
    tomorrow = today.strftime('%d.%m.%Y')

    answer = f'🗓 Расписание на сегодня: \n'
    for i in lessons:
        if i.date == tomorrow:
            answer += (f'Дата:{i.date}\n')
            answer += (f'Номер:{i.number}\n')
            answer += (f'Время:{i.time}\n')
            answer += (f'Тип:{i.way}\n')
            answer += (f'Пара:{i.content}\n')
            answer += (f'--------\n')
    if answer == f'🗓 Расписание на сегодня: \n':
        answer += f'Сегодня нету пар'
    await msg.answer(answer)


class FSMClient(StatesGroup):
    group = State()


async def command_change_group(msg: types.message):
    await FSMClient.group.set()
    await msg.answer('Введите название группы(как на сайте):')


async def change_group(msg: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = msg
    await sqlite_db.change_group_name(msg.chat.id, msg.text)
    await state.finish()
    await msg.reply(f"Имя группы '{msg.text}' сохранено!")

async def command_profile(msg: types.message):
    group_name = await sqlite_db.get_group_name(msg.chat.id)
    id = await sqlite_db.get_id(msg.chat.id)
    await msg.reply(f'Профиль\n'
                    f'ID: {id}\n'
                    f'Группа: {group_name}')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(command_profile, Text(equals='👤Профиль👤', ignore_case=True))
    dp.register_message_handler(command_schedule_today, Text(equals='🗓Расписание на сегодня🗓', ignore_case=True))
    dp.register_message_handler(command_schedule_tomorrow, Text(equals='🗓Расписание на завтра🗓', ignore_case=True))
    dp.register_message_handler(command_schedule_week, Text(equals='🗓Расписание на неделю🗓', ignore_case=True))
    dp.register_message_handler(command_change_group, Text(equals='✏️Сменить группу✏️', ignore_case=True))
    dp.register_message_handler(change_group, state=FSMClient.group)
