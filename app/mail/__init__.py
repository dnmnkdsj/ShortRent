###############################################################################
# Email server module.
###############################################################################
# Provides email service.
# Notice:
# Do *NOT* import this as flask's blueprint.
# Use it as ordinary module.

from flask import current_app as app
from flask_mail import Mail, Message

app.config.update(dict(
    MAIL_SERVER = 'smtp.126.com',
    MAIL_PORT = 465,                # this port number should be 465 which is encoded, not what 163.com says 25.
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'hydroxyapatite@126.com',
    MAIL_PASSWORD = 'hyperoxygen0',
    MAIL_SENDER = 'hydroxyapatite@126.com',
    MAIL_DEFAULT_SENDER = 'hydroxyapatite@126.com'
    ))

mailServer = Mail(app)

