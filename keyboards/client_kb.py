from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton(text='👤Профиль👤')
btn2 = KeyboardButton(text='🗓Расписание на сегодня🗓')
btn3 = KeyboardButton(text='🗓Расписание на завтра🗓')
btn4 = KeyboardButton(text='🗓Расписание на неделю🗓', )
btn5 = KeyboardButton(text='✏️Сменить группу✏️')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(btn1).add(btn2, btn3).add(btn4).add(btn5)
