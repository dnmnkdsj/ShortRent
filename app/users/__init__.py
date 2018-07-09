# Hosues management.

from flask import Blueprint

users = Blueprint('users', __name__, template_folder='templates')

# add more modules if you want..
from . import users_view, users_management
