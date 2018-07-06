# This file manage orders importing, getting a post info from frontend and check permission to write database.

from . import orders
from flask import session, current_app, jsonify, request
from .utils import *

# TODO:
# pages.
orders_management_page = redirect('/test/page')

# TODO:
# exceptions.
order_not_exist_return = jsonify('order does not exists.')
order_is_valid_return = jsonify('the order is already valid.')
order_invalid_return = jsonify('order is invalid.')
order_done_return = jsonify('the order is already completed.')
invalid_valid_parameter_return = jsonify('not specifing the the valid parameter.')
reject_return = jsonify('Done. Remove entry.')
complete_return = jsonify('Done. Entry checkin.')
done_return = jsonify('Successfully set to complete.')

# for administrator management.
@orders.route('/orders/management')
def get_orders_management_page():
    if not check_admin_permission() : return permission_denied_return
    return orders_management_page

# test url: http://127.0.0.1:5000/orders/validate?id=1234568&valid=false
@orders.route('/orders/validate', methods=['GET', 'POST'])
def set_order_valid():
    """
    Provides the operation for validating the orders.
    id: str.
    valid: bool.
    """
    if not check_admin_permission() : return permission_denied_return
    
    data = select_data_source()
    order_id = data['id']
    valid = data['valid']
    
    db = database.getdb()
    
    ### Check if order exists.
    
    cmd = 'select * from orders where id=="{0}"'.format(order_id)
    order_info = db.execute(cmd).fetchall()
    if len(order_info) != 1 :
        return order_not_exist_return
    
    ### Check if order is not valid recently.
    
    cmd = 'select * from orders where id=="{0}" AND passed!=0'.format(order_id)
    order_valid = db.execute(cmd).fetchall()
    print(order_valid)
    if len(order_valid) != 0 :
        return order_is_valid_return
        
    if str.lower(valid) == 'true' :
        ### Set order valid.
        cmd = 'update orders set passed=1 where id=="{0}"'.format(order_id)
        db.execute(cmd)
        db.commit()
        print('set order {0} to valid.'.format(order_id))
        return complete_return
    elif str.lower(valid) == 'false' :
        ### Remove the order entry.
        cmd = 'delete from orders where id="{0}"'.format(order_id)
        db.execute(cmd)
        db.commit()
        print('deny the order {0} and remove it from databse.'.format(order_id))
        # TODO: email something to announce...
        return reject_return
    else:
        return invalid_valid_parameter_return

# test url: http://127.0.0.1:5000/orders/finish?user=947426443@qq.com&id=1234568
@orders.route('/orders/finish', methods=['GET', 'POST'])
def set_order_done():
    """
    Provides the operation for fnishing the orders.
    user: str.
    id: str.
    """
    
    data = select_data_source()
    user = data['user']
    order_id = data['id']
    
    if not check_user_permission(user) : return permission_denied_return
    
    db = database.getdb()
    
    ### Check if is valid.
    
    cmd = 'select passed from orders where id=="{0}"'.format(order_id)
    order_valid = db.execute(cmd).fetchall()[0][0]
    if order_valid == 0 :
        return order_invalid_return
    
    ### Check if is done.
    cmd = 'select done from orders where id=="{0}"'.format(order_id)
    order_done = db.execute(cmd).fetchall()[0][0]
    if order_done != 0 :
        return order_done_return
    
    ### All check done.
    ### Set it to done.
    cmd = 'update orders set done=1 where id=="{0}"'.format(order_id)
    db.execute(cmd)
    db.commit()
    print('user sets order {0} to be done.'.format(user))
    
    return done_return
    