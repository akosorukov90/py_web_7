import asyncio
from email.message import EmailMessage
import aiosmtplib
import sqlite3


SENDER_EMAIL = 'admin@hogmail.local'
TEMPLATE_MESSAGE_EMAIL = f'Уважаемый <имя пользователя>!\nСпасибо, что пользуетесь нашим сервисом объявлений.'
SUBJECT_EMAIL = 'Спасибо, что Вы с нами!'
SMTP_SERVER = 'localhost'
PORT = '1025'


async def send_mail(first_name, last_name, email):
    print(f"Отправка..{email}")
    message = EmailMessage()
    message["From"] = SENDER_EMAIL
    message["To"] = email
    message["Subject"] = SUBJECT_EMAIL
    message.set_content(TEMPLATE_MESSAGE_EMAIL.replace('<имя пользователя>', first_name + ' ' + last_name))

    await aiosmtplib.send(message, hostname=SMTP_SERVER, port=PORT)

    print(f"Отправлено...{email}")


async def main():
    connection = sqlite3.connect('contacts.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.execute('select first_name, last_name, email from contacts')

    users = cur.fetchall()

    await asyncio.gather(*[send_mail(**user) for user in users])


if __name__ == "__main__":
    asyncio.run(main())
