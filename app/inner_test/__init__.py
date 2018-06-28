from flask import Blueprint

inner_test = Blueprint('inner_test', __name__)

from . import test