# Orders management.

from flask import Blueprint, current_app

orders = Blueprint('orders', __name__)

from . import orders_view