# defines all global things used in orders module.

from flask import redirect, request, jsonify
from ..db import database
from . import orders

# TODO:
# change this into some page or so on...
permission_denied_return = 'PERMISSION DENIED'

def check_admin_permission():
    # TODO: enable session.
    # if 'admin' not in session:
    #   return False
    return True

def check_user_permission(username:str):
    # TODO: enable session.
    # things to check:
    # 1. session.username
    # 2. user is valid
    return True

def operate(cmd:str):
    db = database.getdb()
    cur = db.cursor()
    # only support 'orders' table recently.
    cur.execute('select * from orders')
    names = [x[0] for x in cur.description]
    print('run: ' + cmd)
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

def select_data_source():
    data = ''
    if 'form' in request.args and request.args['form'] == 'true' :
        return request.form
    else :
        return request.args
    
# returns a list including (year, month, day).
def get_time(data:str):
    return map(int, data.split('-'))

# returns the day from 1970.1.1
def get_time_days(data:str):
    year, month, day = get_time(data)
    month -= 2
    if 0 >= month :
        month += 12
        year -= 1
    return year // 4 - year // 100 + year // 400 + 367 * month // 12 + day + year * 365 - 719499

# returns a string describes the day time.
def get_time_str(year:int, month:int, day:int):
    return '%02d-%02d-%02d' % (year, month, day)

# standarize time string.
def get_std_time_str(data:str):
    year, month, day = get_time(data)
    return get_time_str(year, month, day)