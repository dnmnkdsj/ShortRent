# this module is only for administrators' management.

from . import orders
from flask import session, current_app, jsonify, request
from ..db import database

from .utils import *

@orders.route('/orders/getinfo', methods=['GET'])
def get_orders_info():
    """
    This method intends to do everything that is to grab data from database.
    Use request['type'] to specify what info you want.
    The info request requires some permission check.
    available types: all, checked, aboutself, owned, ordered, state
    """
    # invoke the bad-request error in advance.
    db = database.getdb()
    
    if request['type'] == 'all' :
        return admin_operate('select * from orders')
    elif request['type'] == 'unchecked' :
        return admin_operate('select * from orders where passed==false')
    elif request['type'] == 'checked' :
        return admin_operate('select * from orders where passed!=false')
    elif request['type'] == 'related' :
        return user_operate('select * from orders where customer=={0} OR owner=={0}')
    elif request['type'] == 'owned' :
        return user_operate('select * from orders where owner=={0}')
    elif request['type'] == 'ordered' :
        return user_operate('select * from orders where customer=={0}')
    elif request['type'] == 'history' :
        return user_operate('select * from orders where customer=={0} AND state=="done"')
    elif request['type'] == 'processing' :
        return user_operate('select * from prders where customer=={0} AND state=="processing"')
    # TODO:
    # Throw an HTTP 400 exception.
    return permission_denied_return
        
