import telebot
import requests
import buttons
import models

bot = telebot.TeleBot('6061662953:AAFLdR-ihJY8seooDIjIzuHZU8InAEVoUbk')


@bot.message_handler(commands=['delphoto'])
def photo_delete(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправте название фото')
    bot.register_next_step_handler(message, get_photo_name_delete)


def get_photo_name_delete(message):
    user_id = message.from_user.id
    photo_name = message.text
    models.delete_photo(photo_name)
    bot.send_message(user_id, 'Успешно удалено')
    bot.register_next_step_handler(message, text)


@bot.message_handler(commands=['photo'])
def photo(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправте название фото')
    bot.register_next_step_handler(message, get_photo_name)


def get_photo_name(message):
    user_id = message.from_user.id
    photo_name = message.text
    bot.send_message(user_id, 'Отпарвте фото')
    bot.register_next_step_handler(message, get_photo, photo_name)


def get_photo(message, photo_name):
    user_id = message.from_user.id
    photo = message.photo
    models.add_photo(photo_name, photo[-1].file_id)
    bot.send_message(user_id, f'Успешно добавлено имя: {photo_name}')
    bot.register_next_step_handler(message, text)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    checker = models.checker(user_id)
    checker_name = models.check_user_name(user_id)
    user_name = message.from_user.first_name
    url = f'https://muhammadkhon.pythonanywhere.com/users/user'
    result = requests.get(url).json()
    result = (result['users'])
    result = ((i['username'])for i in result)
    if checker:
        if checker_name[0] in result:
            bot.send_message(user_id, '*Успешно вошли*', reply_markup=buttons.menu(), parse_mode='MarkDown')
            bot.register_next_step_handler(message, text)

        else:
            bot.send_message(user_id,
                             f'*Добро пожаловать {user_name} в TrendiFY\nСдесь вы можете слушать музыку без рекламы и удобно этот бот алтернатива такого как популярного музыкального проигрывателя Spotify сделан командой SmartDevelopers*',
                             parse_mode='MarkDown')
            bot.send_message(user_id, 'Для регистрации отправте свой Псевдоним[NickName]')
            bot.register_next_step_handler(message, get_password)

    else:
        bot.send_message(user_id,
                         f'*Добро пожаловать {user_name} в TrendiFY\nСдесь вы можете слушать музыку без рекламы и удобно этот бот алтернатива такого как популярного музыкального проигрывателя Spotify сделан командой SmartDevelopers*',
                         parse_mode='MarkDown')
        bot.send_message(user_id, 'Для регистрации отправте свой Псевдоним[NickName]')
        bot.register_next_step_handler(message, get_password)


def get_password(message):
    user_id = message.from_user.id
    nick_name = message.text
    bot.send_message(user_id, 'Теперь придумайте пароль')
    bot.register_next_step_handler(message, registration_get_nick_name, nick_name)


def registration_get_nick_name(message, nick_name):
    password = message.text
    user_id = message.from_user.id
    bot.send_message(user_id, f'Воу, рад знакомству {nick_name}, а теперь отправь свое настояшее Имя')
    bot.register_next_step_handler(message, registration_get_name, nick_name, password)


def registration_get_name(message, nick_name, password):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Теперь отправь Фамилию')
    bot.register_next_step_handler(message, registration_get_last_name, name, nick_name, password)


def registration_get_last_name(message, name, nick_name, password):
    user_id = message.from_user.id
    last_name = message.text
    bot.send_message(user_id, 'Ты почти у цели осталось отправить номер', reply_markup=buttons.get_contact())
    bot.register_next_step_handler(message, registration_get_number, last_name, name, nick_name, password)


def registration_get_number(message, last_name, name, nick_name, password):
    user_id = message.from_user.id
    try:
        number = message.contact.phone_number
        url = f'https://muhammadkhon.pythonanywhere.com/users/user?first_name={name}&password={password}&last_name={last_name}&username={nick_name}&phone_number={number}'
        result = requests.post(url).json()
        print(result)
        models.add_user(user_id, nick_name, password, number, name, last_name)
        bot.send_message(user_id, 'Наслаждайтесь музыкой', reply_markup=buttons.menu())

    except:
        bot.send_message(user_id, 'Воспользуйтесь кнопкой')
        bot.register_next_step_handler(message, registration_get_number, last_name, name, nick_name, password)


@bot.message_handler(content_types=['text'])
def text(message):
    user_id = message.from_user.id
    if message.text == 'Профиль':
        bot.send_message(user_id, 'Ваш профиль', reply_markup=buttons.profile_menu())
        bot.register_next_step_handler(message, profile)

    elif message.text == 'Поиск песни':
        bot.send_message(user_id, 'Отправте название песни')
        bot.register_next_step_handler(message, get_song)

    elif message.text == 'Рекомендуемые':
        url = 'https://muhammadkhon.pythonanywhere.com/songs/song'
        result = requests.get(url).json()
        print(result)
        limit = 0
        for i in result:
            photo = models.view_photo('photo')
            bot.send_photo(user_id, photo[1], f'Название: {i["song_name"]}\nНравистя: {i["song_likes"]}')
            bot.register_next_step_handler(message, text)
            limit += 1
            ind = 10
            if limit == ind:
                break


def profile(message):
    user_id = message.from_user.id
    if message.text == 'Информация':
        result = models.get_all_for_user(user_id)
        print(result)
        bot.send_message(user_id, f'*NickName:* _{result[1]}_\n*Phone:* _{result[2]}_\n*Name:* _{result[3]}_\n'
                                  f'*LastName:* _{result[-1]}_', parse_mode='MarkDown', reply_markup=buttons.menu())
        bot.register_next_step_handler(message, text)

    else:
        bot.send_message(user_id, 'Неверное обрашение')
        bot.register_next_step_handler(message, text)


def get_song(message):
    user_id = message.from_user.id
    music_name = message.text
    url = f'https://muhammadkhon.pythonanywhere.com/songs/{music_name}'
    result = requests.get(url).json()
    print(result)
    try:
        result = (result['song'])
        print(result['song_name'])
        photo = models.view_photo('photo')
        print(photo[0])
        bot.send_photo(user_id, photo[-1], f'Название: {result["song_name"]}\nНравится: {result["song_likes"]}')
        bot.register_next_step_handler(message, text)

    except:
        bot.send_message(user_id, 'Песня не найдена')
        bot.register_next_step_handler(message, text)


bot.polling()
