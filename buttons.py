from telebot import types


def get_contact():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Отправить контакт', request_contact=True)
    kb.add(button)
    return kb


def profile_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Информация')
    kb.add(button1)
    return kb


def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Поиск песни')
    button1 = types.KeyboardButton('Профиль')
    button2 = types.KeyboardButton('Рекомендуемые')
    kb.add(button, button1, button2)
    return kb

