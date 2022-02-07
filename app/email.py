from flask_mail import Mail, Message
from config import Config
from app import mail

def send_verification(recipient, url):
    html = '<a href="{}">Verify Link</a>'.format(url)
    send_email("Email Verification", 
        recipient, 
        "",
        "<h1>Click link to verify account.</h1> {}\n\n".format(html))

def send_email(subject, recipient, body, html):
    msg = Message(subject, sender=Config.MAIL_FROM, 
        recipients=[recipient])
    msg.body = body
    msg.html = html
    mail.send(msg)