from flask import Blueprint, current_app

inner_test = Blueprint('inner_test', __name__)

from . import test
from . import test_mail