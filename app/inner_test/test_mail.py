# test for email sending.

from . import inner_test
from flask import render_template, redirect, url_for
from flask_mail import Mail, Message
from ..mail import mail

@inner_test.route("/test/SendDKEmail")
def mail_main():
    """
    Sample: send DK an email.
    """
    mail.send_email(['947426443@qq.com'], 'Hello!', '!!!', None)
    return redirect(url_for('static', filename='inner_test/DKAvatar.png'))
