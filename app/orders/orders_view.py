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


def operate(cmd:str):
    db = database.getdb()
    cur = db.cursor()
    # only support 'orders' table recently.
    cur.execute('select * from orders')
    names = [x[0] for x in cur.description]
    data = db.execute(cmd).fetchall()
    return jsonify([dict(zip(names, x)) for x in data])

def user_operate(cmd:str):
    username = ''
    if 'username' in request.args :
        username = request.args['username']
    elif 'username' in request.form :
        username = request.form['username']
    if check_admin_permission() or chech_user_permission(username):
        return operate(cmd.format(username))
    return permission_denied_return

def admin_operate(cmd:str):
    if not check_admin_permission() : return permission_denied_return
    return operate(cmd)

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
    
    return jsonify([])    
