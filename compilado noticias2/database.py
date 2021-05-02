import sqlite3 as sql

conn = sql.connect('notices.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS notices(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT, '
               'resume TEXT, date DATETIME)')

cursor.execute('CREATE TABLE IF NOT EXISTS emails(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email TEXT)')

cursor.execute('CREATE TABLE IF NOT EXISTS today_posts(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT, '
               'resume TEXT, date DATETIME)')


def add_notice(title, resume, date):
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notices(title, resume, date) VALUES (?,?,?)', (title, resume, date))
    conn.commit()


def show_notices():
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notices ORDER BY id Desc')
    notices = cursor.fetchall()
    return notices


def verify_date(date):
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM notices")
    dates = cursor.fetchall()
    verify = False
    date = str(date)
    for date_ in dates:
        if date in date_[0]:
            verify = True
            break
    return verify


def save_email(email):
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emails(email) VALUES (?)', (email,))
    conn.commit()


def search_email(email):
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM emails')
    emails = cursor.fetchall()
    verify = False
    for email_ in emails:
        if email in email_[0]:
            verify = True
            break
    return verify


def set_today_news(title, resume, date):
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO today_posts(title, resume, date) VALUES (?,?,?)', (title, resume, date))
    conn.commit()


def delete_today_news():
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM today_posts')
    conn.commit()


def get_today_news():
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM today_posts')
    posts = cursor.fetchall()
    return posts


def verify_today(date):
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date FROM today_posts')
    date_posts = cursor.fetchall()
    date = str(date)
    is_new = False
    for date_ in date_posts:
        if date not in date_[0]:
            is_new = True
            break
    return is_new


def get_mails():
    conn = sql.connect('notices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM emails')
    list_emails = []
    emails = cursor.fetchall()
    for email in emails:
        list_emails.append(email[0])
    return list_emails

