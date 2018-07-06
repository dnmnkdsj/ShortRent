# Houses management.

from flask import Blueprint

houses = Blueprint('houses', __name__)

# add more modules if you want..
from . import houses_management
