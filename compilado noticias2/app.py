from flask import Flask, render_template, request, redirect, url_for
from database import show_notices, save_email, search_email
from main import search_notices, send_mail
import schedule
from threading import Thread
from time import sleep

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notices.sqlite3'
search_notices()

try:
    schedule.every().day.at('21:40').do(send_mail)
except TypeError:
    pass


def loop_schedule():
    while True:
        schedule.run_pending()
        sleep(1)


send = Thread(target=loop_schedule)
send.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/notices', methods=['GET', 'POST'])
def notices():
    notices_ = show_notices()
    return render_template('notices.html', notices=notices_)


@app.route('/data')
def data():
    return render_template('data.html')


@app.route('/data', methods=['POST'])
def data_post():
    email = request.form.get('email')
    verify = search_email(email)
    if verify:
        pass
    else:
        save_email(email)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)


