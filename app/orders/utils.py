# defines all global things used in orders module.

from flask import redirect, request

def check_permission():
    # TODO: enable session.
    # if 'admin' not in session:
    #   return False
    return True

# TODO:
# change this into some page or so on...
permission_denied_return = 'PERMISSION DENIED'

# TODO:
orders_user_page_return = redirect('/test/page')

# TODO:
orders_manager_page_return = redirect('/test/page')

def operate(cmd:str):
    data = db.execute(cmd).fetchall()
    return jsonify(data)

def user_operate(cmd:str):
    username = request.form['username']
    if check_permission() or username == session['username']:
        return operate(cmd.format(username))
    return permission_denied_return

def admin_operate(cmd:str):
    if not check_permission() : return permission_denied_return
        operate(cmd)
