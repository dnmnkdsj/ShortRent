from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager

from config import config


# Create objects
# mail = Mail()
login_manager = LoginManager()


# Factory function
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # All initializing should be written here.
    # this is necessary for properly getting the *app* object when initializing.
    with app.app_context():
        # from .mail import mail
        # app.register_blueprint(bp_inner_test)
        from .users import users as bp_users
        app.register_blueprint(bp_users)
        from .houses import houses as bp_houses
        app.register_blueprint(bp_houses)
        from .orders import orders as bp_orders
        app.register_blueprint(bp_orders)

    # initialize objects
    # mail.init_app(app)
    # login system initialization
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'need login to visit'
    login_manager.session_protection = 'strong'

    return app

