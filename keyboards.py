from telebot import types


# Генерація клавіатури вибору курсу
def course_kb():

    values = (('1 курс', '1'), ('2 курс', '2'), ('3 курс', '3'), ('4 курс', '4'),
              ('1 курс скороч.', '1st'), ('2 курс скороч.', '2st'), ('1 курс магістр', '1mg'),)
    buttons = [types.InlineKeyboardButton(text=value[0], callback_data=value[1]) for value in values]
    return buttons


# Генерація клавіатури оновлення курсу
def update_course_kb():
    kb = types.InlineKeyboardMarkup()
    values = (('1 курс', 'update__1'), ('2 курс', 'update__2'), ('3 курс', 'update__3'), ('4 курс', 'update__4'),
              ('1 курс скороч.', 'update__1st'), ('2 курс скороч.', 'update__2st'), ('1 курс магістр', 'update__1mg'),)
    buttons = [types.InlineKeyboardButton(text=value[0], callback_data=value[1]) for value in values]
    kb.add(*buttons)
    return kb


# Генерація клавіатури вибору групи
def group_kb():
    values = (('КІ', 'group_KI'), ('БЦІ', 'group_BCI'), ('ПМ', 'group_PM'), ('АКІT', 'group_AKIT'),
              ('ЕЛ', 'group_EL'))
    buttons = [types.InlineKeyboardButton(text=value[0], callback_data=value[1]) for value in values]

    return buttons


# Генерація клавіатури оновлення групи
def update_group_kb():
    kb = types.InlineKeyboardMarkup()
    values = (('КІ', 'update_KI'), ('БЦІ', 'update_BCI'), ('ПМ', 'update_PM'), ('АКIT', 'update_AKIT'),
              ('ЕЛ', 'update_EL'))
    buttons = [types.InlineKeyboardButton(text=value[0], callback_data=value[1]) for value in values]
    kb.add(*buttons)
    return kb


# Генерація клавіатури головного меню
def menu_kb():
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('Розклад', 'Нагадування')
    keyboard.row('Одногрупники', 'Бесіда')
    keyboard.row('Налаштування')
    return keyboard


# Генерація клавіатури підменю розклад
def schedule_kb():
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('На сьогодні', 'На тиждень', 'Екзамени', 'Модуль')
    return keyboard


# Генерація клавіатури підменю  налаштування
def settings_kb():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Ім\'я', 'Прізвище')
    keyboard.row('Пошта', 'Тиждень')
    keyboard.row('Спеціальність', 'Курс')
    keyboard.row('Назад')
    return keyboard


# Генерація клавіатури підменю нагадування
def alert_kb():
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('На сьогодні', 'Інша дата')
    return keyboard
