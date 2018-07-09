# Houses management.

from flask import Blueprint

houses = Blueprint('houses', __name__)

# add more modules if you want..
from . import check_house, house_info, publish_house, search_house, show_house
