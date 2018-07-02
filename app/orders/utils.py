# defines all global things used in orders module.

from flask import redirect, request, jsonify
from ..db import database

# TODO:
orders_page = '/test/page'
orders_management_page = '/test/page'

# TODO:
# change this into some page or so on...
permission_denied_return = 'PERMISSION DENIED'

# TODO:
orders_user_page_return = redirect('/test/page')

# TODO:
orders_manager_page_return = redirect('/test/page')

def operate(cmd:str):
    db = database.getdb()
    print('run: ' + cmd)
    data = db.execute(cmd).fetchall()
    return jsonify(data)

def check_admin_permission():
    # TODO: enable session.
    # if 'admin' not in session:
    #   return False
    return True

def user_operate(cmd:str):
    username = ''
    if 'username' in request.args :
        username = request.args['username']
    elif 'username' in request.form :
        username = request.form['username']
    if check_admin_permission() or username == session[username]:
        return operate(cmd.format(username))
    return permission_denied_return

def admin_operate(cmd:str):
    if not check_admin_permission() : return permission_denied_return
    return operate(cmd)

