import json
import datetime

import pandas as pd
import numpy as np

chats = {
    '1': {
        'KI': 'https://t.me/joinchat/exP2RH3Fa2FlZmQ6',
        'BCI': 'https://t.me/joinchat/NaF0hbtC-3Q1OGMy',
        'PM': 'https://t.me/joinchat/D4ZbEPWfyyszMTNi',
        'AKIT': 'https://t.me/joinchat/LGjASMNq2xxkNTAy',
        'EL': 'https://t.me/joinchat/bXwrAYfX_ZdmNWYy',
    },
    '2': {
        'KI': 'https://t.me/joinchat/5qwmB-eetlw5M2Fi',
        'BCI': 'https://t.me/joinchat/P7LAskHUdLo3OWIy',
        'PM': 'https://t.me/joinchat/NHL7kESzhnRlNjM6',
        'AKIT': 'https://t.me/joinchat/hchB6eVrCwY1Y2Vi',
        'EL': 'https://t.me/joinchat/DM84R9k9HZg3YWFi',
    },
    '3': {
        'KI': 'https://t.me/joinchat/9aam_QZFIUEzZGEy',
        'BCI': 'https://t.me/joinchat/PgkHkcaCSkQ4Mzdi',
        'PM': 'https://t.me/joinchat/8PJh8l2TXKc2YmEy',
        'AKIT': 'https://t.me/joinchat/U21YkmbSdyBkM2Fi',
        'EL': 'https://t.me/joinchat/eBfIt0y_nshhZTZi',
    },
    '4': {
        'KI': 'https://t.me/joinchat/3rtcrHKeUXs0Y2Ni',
        'BCI': 'https://t.me/joinchat/FCm_JUAwMvpkMmRi',
        'PM': 'https://t.me/joinchat/xWKKI8dDrcAxMGIy',
        'AKIT': 'https://t.me/joinchat/2yKXPjVlBIs3Njli',
        'EL': 'https://t.me/joinchat/BDVNZEa0NCk3MWQy',
    },
    '1mg': {
        'KI': 'https://t.me/joinchat/d0qNroVkX_M1OWUy',
        'BCI': 'https://t.me/joinchat/WenSiLb_lb03ZjNi',
        'PM': 'https://t.me/joinchat/xsdlc4GM-ww4ODRi',
        'AKIT': 'https://t.me/joinchat/LjkPJLY57VxlMDEy',
        'EL': 'https://t.me/joinchat/v2aEkLkGgm01Yjdi',
    },
    '1st': {
        'KI': 'https://t.me/joinchat/exP2RH3Fa2FlZmQ6',
        'BCI': 'https://t.me/joinchat/NaF0hbtC-3Q1OGMy',
        'PM': 'https://t.me/joinchat/D4ZbEPWfyyszMTNi',
        'AKIT': 'https://t.me/joinchat/LGjASMNq2xxkNTAy',
        'EL': 'https://t.me/joinchat/bXwrAYfX_ZdmNWYy',
    },
    '2st': {
        'KI': 'https://t.me/joinchat/5qwmB-eetlw5M2Fi',
        'BCI': 'https://t.me/joinchat/P7LAskHUdLo3OWIy',
        'PM': 'https://t.me/joinchat/NHL7kESzhnRlNjM6',
        'AKIT': 'https://t.me/joinchat/hchB6eVrCwY1Y2Vi',
        'EL': 'https://t.me/joinchat/DM84R9k9HZg3YWFi',
    }
}


def read_schedule(user):

    week = {1: '1week', 2: '2week'}
    course = {'1': '1course.xlsx', '2': '2course.xlsx', '3': '3course.xlsx', '4': '4course.xlsx',
              '1mg': '1mg_course.xlsx', '1st': '1st_course.xlsx', '2st': '2st_course.xlsx',
              }
    file_name = week[user[3]] + '/' + course[user[1]]
    df = pd.read_excel(file_name, sheet_name=user[2])
    df = df.rename(columns={'Unnamed: 0': 'День', 'Unnamed: 1': 'Предмет', 'Unnamed: 2': 'Викладач'})
    df['День'][0:5] = 'ПОНЕДІЛОК'
    df['День'][5:10] = 'ВІВТОРОК'
    df['День'][10:15] = 'СЕРЕДА'
    df['День'][15:20] = 'ЧЕТВЕР'
    df['День'][20:25] = 'П’ЯТНИЦЯ'

    return df


# Розклад на тиждень
def week_schedule(df_sched):
    result = ''
    i = 1

    for index, series in df_sched.iterrows():
        if index % 5 == 0:
            result += series['День'] + ':\n'
            i = 1
        if series['Предмет'] is np.nan:
            result += str(i) + ' - Немає пари' + ';\n'
        else:
            result += str(i) + ' - ' + series['Предмет'] + ' - ' + series['Викладач'] + ';\n'
        i += 1
    while i <= 5:
        result += str(i) + ' - Немає пари'';\n'
        i += 1
    return result


# Розклад на день
def day_schedule(df_sched):
    result = ''
    days = {'Mon': 'ПОНЕДІЛОК', 'Tue': 'ВІВТОРОК', 'Wed': 'СЕРЕДА', 'Thu': 'ЧЕТВЕР', 'Fri': 'П’ЯТНИЦЯ'}
    today = datetime.datetime.now()
    today = today.strftime("%a")

    df_day = df_sched[df_sched['День'] == days[today]]
    i = 0
    for index, series in df_day.iterrows():
        i += 1
        if series['Предмет'] is np.nan:
            result += str(i) + ' - Немає пари' + ';\n'
        else:
            result += str(i) + ' - ' + series['Предмет'] + ' - ' + series['Викладач'] + ';\n'
    if i == 1:
        result = 'Немає пар'
    return result


# Розклад для нагадування
def day_reminder(df_sched):
    days = {'Mon': 'ПОНЕДІЛОК', 'Tue': 'ВІВТОРОК', 'Wed': 'СЕРЕДА', 'Thu': 'ЧЕТВЕР', 'Fri': 'П’ЯТНИЦЯ'}
    today = datetime.datetime.now()
    today = today.strftime("%a")
    df_day = df_sched[df_sched['День'] == days[today]]

    result = []

    for index, series in df_day.iterrows():

        if series['Предмет'] is np.nan:
            result.append('Немає пари')
        else:
            result.append(series['Предмет'] + ' - ' + series['Викладач'])

    return result


def get_tg_chat(group, course):
    return chats[course][group]
