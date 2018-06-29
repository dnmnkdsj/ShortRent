# Hosues management.

from flask import Blueprint

users = Blueprint('users', __name__)

# add more modules if you want..
from . import users_management
