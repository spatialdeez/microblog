from flask_mail import Message # type: ignore
from flask import render_template
from app import app, mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_reset_password_email(user):
    token = user.get_reset_password_token()
    send_email(
        subject='[Microblog] Password reset request',
        sender=app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
    )