from flask import Flask
from .inner_test import inner_test as bp_inner_test

app = Flask(__name__)
app.register_blueprint(bp_inner_test)
