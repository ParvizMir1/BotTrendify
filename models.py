import sqlite3

connection = sqlite3.connect('TrendiFY.db')
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users'
            '(telegram_id INTEGER, nick_name TEXT, password TEXT,phone_number TEXT, first_name TEXT, last_name TEXT);')

sql.execute('CREATE TABLE IF NOT EXISTS photo (photo_name TEXT, photo_id TEXT);')


def add_photo(photo_name, photo_id):
    connection = sqlite3.connect('TrendiFY.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO photo VALUES (?,?)', (photo_name, photo_id))

    connection.commit()


def view_photo(photo_name):
    connection = sqlite3.connect('TrendiFY.db')
    sql = connection.cursor()

    result = sql.execute('SELECT * FROM photo WHERE photo_name=?;', (photo_name,)).fetchone()

    return result


def delete_photo(photo_name):
    connection = sqlite3.connect('TrendiFY.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM photo WHERE photo_name=?;', (photo_name,))

    connection.commit()


#ADD user in db
def add_user(user_id, nick_name, password,phone_number, first_name, last_name):
    connection = sqlite3.connect('TrendiFY.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO users VALUES (?,?,?,?,?,?)', (user_id, nick_name, password, phone_number, first_name, last_name))

    connection.commit()


#Check User in db
def checker(user_id):
    connection = sqlite3.connect('TrendiFY.db')
    sql = connection.cursor()

    result = sql.execute('SELECT telegram_id FROM users WHERE telegram_id=?', (user_id,)).fetchone()

    if result:
        return True

    else:
        return False


def check_user_name(user_id):
    connection = sqlite3.connect('TrendiFY.db')
    sql = connection.cursor()

    result = sql.execute('SELECT nick_name FROM users WHERE telegram_id=?', (user_id,)).fetchone()

    return result


def get_all_for_user(user_id):
    connection = sqlite3.connect('TrendiFY.db')
    sql = connection.cursor()

    result = sql.execute('SELECT * FROM users WHERE telegram_id=?', (user_id,)).fetchone()

    return result

