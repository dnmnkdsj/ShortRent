# defines all global things used in orders module.

from flask import redirect, request, jsonify, session
from ..db import database
from . import orders

# TODO:
# change this into some page or so on...
permission_denied_return = jsonify([-1, 'PERMISSION DENIED'])

def check_admin_permission() :
    return session.get('admin', 0) != 0

def check_user_permission(username:str) :
    if check_admin_permission() : return True
    db = database.getdb()
    cmd = 'select * from users where mail="{0}" AND valid=1'.format(username)
    info = db.execute(cmd).fetchall()
    if len(info) == 0 : return False
    return session.get('_id', '') == username

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