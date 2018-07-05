from flask import Flask

app = Flask(__name__)

# All initializing should be written here.
# this is necessary for properly getting the *app* object when initializing.
with app.app_context():
    from .mail import mail
    app.register_blueprint(bp_inner_test)
    from .users import users as bp_users
    app.register_blueprint(bp_users)
    from .houses import houses as bp_houses
    app.register_blueprint(bp_houses)
    from .orders import orders as bp_orders
    app.register_blueprint(bp_orders)

