# This file manage orders importing, getting a post info from frontend and check permission to write database.

from . import orders
from flask import session, current_app, jsonify, request
from .utils import *

# TODO:
# pages.
orders_management_page = redirect('/test/page')

# Results for validating orders.
validate_complete_return = jsonify([0, 'Done. Entry checkin.'])
validate_not_exist_return = jsonify([1, 'order does not exists.'])
validate_invalid_user_return = jsonify([2, 'User does not related to this order.'])
validate_is_valid_return = jsonify([3, 'the order is already valid.'])
validate_conflict_return = jsonify([4, "another order at the same time is already valid."])
validate_reject_return = jsonify([5, 'Done. Remove entry.'])
validate_valid_parameter_error_return = jsonify([6, 'not specifing the the valid parameter.'])

finish_complete_return = jsonify([0, 'Successfully set to complete.'])
finish_invalid_return = jsonify([1, 'order is invalid.'])
finish_done_return = jsonify([2, 'the order is already completed.'])

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
    user: str.
    """
    data = select_data_source()
    order_id = data['id']
    valid = data['valid']
    user = data['user']
    
    if not check_user_permission(user) : return permission_denied_return
    
    db = database.getdb()
    
    ### Check if order exists.
    
    cmd = 'select * from orders where id=="{0}"'.format(order_id)
    order_info = db.execute(cmd).fetchall()
    if len(order_info) != 1 :
        return validate_not_exist_return
    
    ### Check if this order belongs to the user.
    
    cmd = 'select * from orders where id=="{0}" AND owner=="{1}"'.format(order_id, user)
    user_info = db.execute(cmd).fetchall()
    if len(user_info) != 1 :
        return validate_invalid_user_return
    
    ### Check if order is not valid recently.
    
    cmd = 'select * from orders where id=="{0}" AND passed!=0'.format(order_id)
    order_valid = db.execute(cmd).fetchall()
    if len(order_valid) != 0 :
        return validate_is_valid_return
    
    ### Check if there is an order already valid at the same time.
    cmd = 'select time from orders where id=="{0}"'.format(order_id)
    order_time = db.execute(cmd).fetchall()[0][0]
    cmd = 'select * from orders where time=="{0}" AND passed!=0'.format(order_time)
    conflict = db.execute(cmd).fetchall()
    if len(conflict) != 0 :
        return validate_conflict_return
    
    if str.lower(valid) == 'true' :
        ### Set order valid.
        cmd = 'update orders set passed=1 where id=="{0}"'.format(order_id)
        db.execute(cmd)
        db.commit()
        print('set order {0} to valid.'.format(order_id))
        return validate_complete_return
    elif str.lower(valid) == 'false' :
        ### Remove the order entry.
        cmd = 'delete from orders where id="{0}"'.format(order_id)
        db.execute(cmd)
        db.commit()
        print('deny the order {0} and remove it from databse.'.format(order_id))
        # TODO: email something to announce...
        return validate_reject_return
    else:
        return validate_valid_parameter_error_return

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
        return finish_invalid_return
    
    ### Check if is done.
    cmd = 'select done from orders where id=="{0}"'.format(order_id)
    order_done = db.execute(cmd).fetchall()[0][0]
    if order_done != 0 :
        return finish_done_return
    
    ### All check done.
    ### Set it to done.
    cmd = 'update orders set done=1 where id=="{0}"'.format(order_id)
    db.execute(cmd)
    db.commit()
    print('user sets order {0} to be done.'.format(user))
    
    return finish_complete_return
    