from flask_mail import Mail, Message
from config import Config
from app import mail

def send_email(subject, recipient, body, html):
    msg = Message(subject, sender=Config.MAIL_USERNAME, recipients=[recipient])
    msg.body = body
    msg.html = html
    mail.send(msg)