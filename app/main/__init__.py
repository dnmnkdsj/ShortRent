from flask import Blueprint

'''
This is the main blurprint
'''

main = Blueprint('main', __name__)

from . import views
