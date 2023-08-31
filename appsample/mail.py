########
# reference:https://github.com/twtrubiks/Flask-Mail-example
#           https://hackmd.io/@shaoeChen/BytvGKs4M?type=view#
########

from threading import Thread

from celery import shared_task
from flask import current_app, render_template
from flask_mail import Message

from . import email


def send_async_email(app, msg):
    """
    取得了app跟msg兩個物件之後，利用了app.app_context來讓整個程序是在一個程序的上下文內，這是flask-mail中的send的限制。
    雖然兩個物件都是從context中傳來的，但是因為開了另一個新的thread，所以必需手動將物件放入一個程序上下文中。
    """
    with app.app_context():
        email.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@shared_task(ignore_result=False)
def send_email_celery(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    with app.app_context():
        email.send(msg)
