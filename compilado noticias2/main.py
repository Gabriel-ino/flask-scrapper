from bs4 import BeautifulSoup
import requests
from datetime import datetime
from database import add_notice, verify_date, set_today_news, verify_today, delete_today_news, get_mails, get_today_news
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def search_notices():
    sites = ['site1', 'site2',
             'site3', 'site4']
    html = [requests.get(site).content for site in sites]
    notices = []
    count = 0
    today = datetime.today().utcnow().date()

    for site in sites:
        soup = BeautifulSoup(html[count], 'html.parser')
        if '' in site:
            notice = soup.find('a', class_="HTML_CLASS").string
            resume = soup.find('div', class_="HTML_CLASS").string
            notices.append([notice, resume])

        elif '' in site:
            notice = soup.find('span', class_="HTML_CLASS").string
            resume = soup.find('p', class_="HTML_CLASS").string
            notices.append([notice, resume])
        elif '' in site:
            notice = soup.find('h2', class_="HTML_CLASS").string
            resume = soup.find('p', class_="HTML_CLASS").string
            notices.append([notice, resume])

        elif '' in site:
            notice = soup.find('a', class_="HTML_CLASS").string
            resume = soup.find('div', class_="HTML_CLASS").string
            notices.append([notice, resume, today])

        count += 1

    verify = verify_date(today)
    for notice_ in notices:
        if verify:
            pass
        if not verify:
            add_notice(notice_[0], notice_[1], today)
            set_today_news(notice_[0], notice_[1], today)
            verify_today_post = verify_today(today)
            if not verify_today_post:
                pass
            else:
                delete_today_news()
                set_today_news(notice_[0], notice_[1], today)


def send_mail():
    email_list = get_mails()
    email_from = os.getenv('EMAIL')
    email_password = os.getenv('PASSWORD')
    email_smtp = 'smtp.gmail.com'
    destination = email_list
    subject = 'Noticias diarias'

    message = MIMEMultipart()
    message['FROM'] = email_from
    message['SUBJECT'] = subject
    message['To'] = ", ".join(destination)

    text = ''
    notices = get_today_news()
    for notice in notices:
        text += f'<b>{notice[1]}</b>' + '<br>' + f'{notice[2]}' + '<br><br>'

    msg_text = MIMEText(text, 'html')
    message.attach(msg_text)
    try:
        smtp = smtplib.SMTP(email_smtp, 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email_from, email_password)
        smtp.sendmail(email_from, destination, message.as_string())
        print('Email enviado com sucesso')
    except Exception as e:
        print(f'Falha ao enviar email: {e}')
