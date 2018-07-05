###############################################################################
# Email server module.
###############################################################################
# Provides email service.
# Notice:
# Do *NOT* import this as flask's blueprint.
# Use it as ordinary module.

from flask import current_app as app
from flask_mail import Mail

mailServer = Mail(app)
