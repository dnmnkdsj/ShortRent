# this file provides function to grab info from database and deliver to the frontpage.

from . import orders
from flask import request
from .utils import *

# TODO:
orders_page = redirect('/test/page')

# page for displaying orders and other info.
@orders.route('/orders')
def get_orders_page():
    return orders_page

# this url is for grabbing data only.
@orders.route('/orders/getinfo', methods=['GET'])
def get_orders_info():
    """
    This method intends to do everything that is to grab data from database.
    Use request.args['type'] to specify what info you want.
    The info request requires some permission check.
    sample html: /orders/getinfo?type=all&username=aaa
    sample html for submitting form: /orders/getinfo?form=true
    available types: all, checked, aboutself, owned, ordered, state
    """
    type = ''
    if 'form' in request.args and request.args['form'] == 'true' :
        type = request.form['type']
    else :
        type = request.args['type']
    
    # invoke the bad-request error in advance.
    if type == 'all' :
        return admin_operate('select * from orders')
    elif type == 'unchecked' :
        return admin_operate('select * from orders where passed=="false"')
    elif type == 'checked' :
        return admin_operate('select * from orders where passed!="false"')
    elif type == 'related' :
        return user_operate('select * from orders where customer=="{0}" OR owner=="{0}"')
    elif type == 'owned' :
        return user_operate('select * from orders where owner=="{0}"')
    elif type == 'ordered' :
        return user_operate('select * from orders where customer=="{0}"')
    elif type == 'done' :
        return user_operate('select * from orders where ( customer=="{0}" OR owner=="{0}" ) AND done==1')
    elif type == 'processing' :
        return user_operate('select * from orders where ( customer=="{0}" OR owner=="{0}" ) AND done==0')
    # TODO:
    # Throw an HTTP 400 exception.
    return permission_denied_return
        
