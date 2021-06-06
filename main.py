import datetime
import json
import threading
import time

import telebot
from telebot import types
import schedule

import config
import db
from keyboards import *
from my_sched import *
# створення бота
bot = telebot.AsyncTeleBot(config.token)


# фоновый режим для нагадувань
def run_continuously(interval=1):

    cease_continuous_run = threading.Event()

    # нагадування у потоках
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


# отримання тижневого розкладу
def get_week_schedule(message):

    user_data = db.get_schedule(message.from_user.id)
    result = week_schedule(read_schedule(user_data))

    return result


# отримання денного розкладу
def get_day_schedule(message):

    user_data = db.get_schedule(message.from_user.id)
    result = day_schedule(read_schedule(user_data))

    return result


# створення користувача - ФІО
def create_user(message):
    try:
        name, surname = message.text.split()
    except ValueError:
        bot.send_message(message.chat.id, f"Введи через пробіл, наприклад Іван Іванов")
        bot.register_next_step_handler(message, create_user)
    db.add_user([message.from_user.id, name, surname, message.chat.username])

    kb = types.InlineKeyboardMarkup()
    kb.add(*course_kb())

    bot.send_message(message.chat.id, f"Я тебе запам'ятав, {name}\n Який ти курс?", reply_markup=kb)


# Команда Старт - початок роботи боту
@bot.message_handler(commands=["start"])
def start_message(message):

    bot.send_message(message.chat.id, "Привіт, будемо навчатись разом!\nЯк тебе звати? (Ім'я та Прізвище)", )
    bot.register_next_step_handler(message, create_user)


# Функція отримання курсу
@bot.callback_query_handler(func=lambda call: call.data[0].isdigit())
def get_course(call):
    db.add_course([call.from_user.id, call.data])

    kb = types.InlineKeyboardMarkup()
    kb.add(*group_kb())
    bot.send_message(call.message.chat.id, f"А яка в тебе спеціальність ?", reply_markup=kb)


# Функція отримання спеціальності
@bot.callback_query_handler(func=lambda call: call.data.startswith('group_'))
def get_group(call):
    group = str(call.data)[call.data.index('group_') + 6:]

    db.add_group([call.from_user.id, group])

    kb = types.InlineKeyboardMarkup()
    week_1 = types.InlineKeyboardButton(text="1", callback_data="one")
    week_2 = types.InlineKeyboardButton(text="2", callback_data="two")
    kb.add(week_1, week_2)
    bot.send_message(call.message.chat.id, "Який зараз варіант тиждня?", reply_markup=kb)


# Функція отримання тиждня та початок роботи
@bot.callback_query_handler(func=lambda call: call.data in ['one', 'two'])
def get_week(call):
    if call.data == "one":
        db.add_week([call.from_user.id, 1])
    elif call.data == "two":
        db.add_week([call.from_user.id, 2])

    bot.send_message(call.message.chat.id, "Я до твоїх послуг!", reply_markup=menu_kb())


# Функція оновлення курсу
@bot.callback_query_handler(func=lambda call: call.data.startswith('update__'))
def update_course(call):
    course = str(call.data)[call.data.index('update__') + 8:]

    db.add_course([call.from_user.id, course])
    bot.send_message(call.message.chat.id, f"Курс оновлен {course}", reply_markup=menu_kb())


# Функція оновлення групи
@bot.callback_query_handler(func=lambda call: call.data.startswith('update_'))
def update_group(call):
    group = str(call.data)[call.data.index('update_') + 7:]

    db.add_group([call.from_user.id, group])
    bot.send_message(call.message.chat.id, f"Спеціальність оновленна {group}", reply_markup=menu_kb())


# Функція оновлення тиждня
@bot.callback_query_handler(func=lambda call: call.data.startswith('u_'))
def update_week(call):
    week = str(call.data)[call.data.index('u_') + 2:]

    if week == "one":
        week = 1
    elif week == "two":
        week = 2

    db.add_week([call.from_user.id, week])
    bot.send_message(call.message.chat.id, f"Тиждень оновленно на {week}", reply_markup=menu_kb())


# Функція отримання команд головного меню
@bot.message_handler(content_types=["text"])
def get_text(message):

    buttons = ('розклад', 'нагадування', 'одногрупники', 'бесіда', 'налаштування')
    trigger = message.text.lower()
    # опрацювання кнопок меню
    if trigger in buttons:
        # опрацювання кнопки розклад
        if trigger == buttons[0]:
            bot.send_message(message.chat.id, "Який розклад бажаєш?", reply_markup=schedule_kb())
            bot.register_next_step_handler(message, check_schedule_comm)
        # опрацювання кнопки нагадування
        elif trigger == buttons[1]:
            msg = 'В тебе є одне нагадування!\nСтворити на сьогодні чи іншу дату ?'
            bot.send_message(message.chat.id, msg, reply_markup=alert_kb())
            bot.register_next_step_handler(message, create_remind)
        # опрацювання кнопки список одногруппників
        elif trigger == buttons[2]:
            students = db.get_user_group(message.chat.id)
            data = ''
            for stu in students:
                data += f'Студент: {stu[0]}  {stu[1]} \n Пошта: {stu[2]}\n Телеграм: @{stu[3]}\n'
                data += '-'*10 + '\n'
            bot.send_message(message.chat.id, data, reply_markup=menu_kb())
        # опрацювання кнопки посилання на чат
        elif trigger == buttons[3]:
            user_data = db.get_schedule(message.chat.id)
            course, group = user_data[1:3]
            data = get_tg_chat(group, course)
            bot.send_message(message.chat.id, data, reply_markup=menu_kb())
        # опрацювання кнопки налаштування
        elif trigger == buttons[4]:
            msg = "У налаштуваннях можна додати:\n" \
                  "Ім'я, Прізвище та Пошту. \n " \
                  "Вибрати тиждень або змінити спеціальність та курс"
            bot.send_message(message.chat.id, msg, reply_markup=settings_kb())
            bot.register_next_step_handler(message, do_settings)


# Функція підменю розкладу, вибір розкладу
def check_schedule_comm(message):
    if message.text.lower() == 'на сьогодні':
        today = datetime.datetime.now()
        today = today.strftime("%a")
        if today in ('Sat', 'Sun'):
            bot.send_message(message.chat.id, 'Сьогодні вихідний', reply_markup=menu_kb())
            return
        data = get_day_schedule(message)
    elif message.text.lower() == 'на тиждень':

        data = get_week_schedule(message)
    elif message.text.lower() == 'екзамени':

        data = 'https://drive.google.com/file/d/1RJzbSm_w4gInGrnBz0jpYkOwuNzPqkaP/view?usp=sharing'
    elif message.text.lower() == 'модуль':

        data = 'https://drive.google.com/file/d/1zIFko09OBJNZfoeHkG3cJWXFdU5DwROY/view?usp=sharing'
    else:
        data = 'Я тебе не розумію'

    bot.send_message(message.chat.id, data, reply_markup=menu_kb())


# Функція підменю  нагадування
def create_remind(message):
    if message.text.lower() == 'на сьогодні':

        bot.send_message(message.chat.id, 'Введи нагадування в форматі  " 00:00 - текст нагадування "')
        bot.register_next_step_handler(message, create_note_today)

    elif message.text.lower() == 'інша дата':

        bot.send_message(message.chat.id, 'Введи нагадування в форматі   " 00.00 (дата 28.08) 00:00 (час) - текст нагадування "')
        bot.register_next_step_handler(message, create_note_date)

# Функція створення нагадування на сьогодні
def create_note_today(message):
    try:
        note_time, note = message.text.split('-')
    except:
        bot.send_message(message.chat.id, 'Введи через дефіс', reply_markup=menu_kb())

    def job(chat_id, text):
        bot.send_message(chat_id, text, reply_markup=menu_kb())
        return schedule.CancelJob

    schedule.every().day.at(note_time.strip()).do(job, chat_id=message.chat.id, text=note)
    bot.send_message(message.chat.id, 'Я нагадаю тобі', reply_markup=menu_kb())


# Функція створення нагадування на дату
def create_note_date(message):
    try:
        note_datetime, note = message.text.split('-')
    except:
        bot.send_message(message.chat.id, 'Введи через дефіс', reply_markup=menu_kb())
    note_date, note_time = note_datetime.split()

    def job(chat_id, text, day):
        now = datetime.datetime.now().date()
        if day.day == now.day and day.month == now.month:
            bot.send_message(chat_id, text, reply_markup=menu_kb())
            return schedule.CancelJob
    note_date = datetime.datetime.strptime(note_date, '%d.%m')
    schedule.every().day.at(note_time.strip()).do(job, chat_id=message.chat.id, text=note, day=note_date)
    bot.send_message(message.chat.id, 'Я нагадаю тобі', reply_markup=menu_kb())


# Функція обробки підменю налаштування
def do_settings(message):
    trigger = message.text.lower()

    if trigger == "ім'я":
        bot.send_message(message.chat.id, f"Назви свое нове ім'я")
        bot.register_next_step_handler(message, update_name)

    elif trigger == "прізвище":
        bot.send_message(message.chat.id, f"Назви нове прізвище")
        bot.register_next_step_handler(message, update_surname)

    elif trigger == "пошта":
        bot.send_message(message.chat.id, f"Назви нову пошту")
        bot.register_next_step_handler(message, update_email)

    elif trigger == "тиждень":
        kb = types.InlineKeyboardMarkup()
        week_1 = types.InlineKeyboardButton(text="1", callback_data="u_one")
        week_2 = types.InlineKeyboardButton(text="2", callback_data="u_two")
        kb.add(week_1, week_2)
        bot.send_message(message.chat.id, f"Назви новий тиждень", reply_markup=kb)

    elif trigger == "група":
        bot.send_message(message.chat.id, f"Назви нову спеціальність", reply_markup=update_group_kb())

    elif trigger == "курс":
        bot.send_message(message.chat.id, f"Назви новий курс", reply_markup=update_course_kb())
    elif trigger == "назад":
        bot.delete_message(message.chat.id, message.message_id)
        data = 'Головне меню'
        bot.send_message(message.chat.id, data, reply_markup=menu_kb())
    else:
        data = 'Я тебе не розумію'
        bot.send_message(message.chat.id, data, reply_markup=menu_kb())


# Функція оновлення ім'я
def update_name(message):
    db.add_firstName([message.from_user.id, message.text])
    bot.send_message(message.chat.id, f"Готово, нове ім'я {message.text}", reply_markup=menu_kb())


# Функція оновлення прізвища
def update_surname(message):
    db.add_lastName([message.from_user.id, message.text])
    bot.send_message(message.chat.id, f"Готово, нове прізвище {message.text}", reply_markup=menu_kb())


# Функція оновлення пошти
def update_email(message):
    db.add_email([message.from_user.id, message.text])
    bot.send_message(message.chat.id, f"Готово, нова пошта {message.text}", reply_markup=menu_kb())


# Функція для нагадування по часу
def reminder():
    user_data = db.get_all()
    lesson = {'07:50': 0, '09:25': 1, '10:55': 2, '12:55': 3, '14:25': 4}

    for user in user_data:
        schedule_rem = day_reminder(read_schedule(user))[lesson[datetime.datetime.now().strftime('%H:%M')]]
        if schedule_rem == '':
            schedule_rem = f"{lesson[datetime.datetime.now().strftime('%H:%M')]} - Пари немає"
        bot.send_message(user[0], schedule_rem)


# Функція, запису задач про нагадування
def days_reminder():
    schedule.every().day.at('07:50').do(reminder)
    schedule.every().day.at('09:25').do(reminder)
    schedule.every().day.at('10:55').do(reminder)
    schedule.every().day.at('12:55').do(reminder)
    schedule.every().day.at('14:25').do(reminder)


# Программне тіло модулю
if __name__ == '__main__':
    days_reminder()  # запис задач
    stop_run_continuously = run_continuously()  # запуск нагадування у фоновому режимі
    db.init_db()  # Підключення до бази даних
    bot.infinity_polling()  # запуск бота
    stop_run_continuously.set()  # Вимкнення нагадувань
