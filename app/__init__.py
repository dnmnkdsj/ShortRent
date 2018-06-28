from flask import Flask

app = Flask(__name__)

# All initializing should be written here.
# this is necessary for properly getting the *app* object when initializing.
with app.app_context():
    from .mail import mail
    from .inner_test import inner_test as bp_inner_test
    app.register_blueprint(bp_inner_test)

