# This file manage orders importing, getting a post info from frontend and check permission to write database.

from . import orders
from flask import session, current_app, jsonify, request
from .utils import *
from flask_login import login_required

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

ranking_complete_return = jsonify([0, 'Done.'])
ranking_not_exist_return = jsonify([1, 'Order does not exist.'])
ranking_not_relative_return = jsonify([2, 'User cannot rank on this order.'])
ranking_already_ranked_return = jsonify([3, 'Already ranked.'])
ranking_invalid_value_return = jsonify([4, 'Ranking value is not valid.'])

# for administrator management.
@orders.route('/orders/management')
def get_orders_management_page():
    if not check_admin_permission() : return permission_denied_return
    return orders_management_page
    
#######################################################################################################################
#######################################################################################################################

# test url: http://127.0.0.1:5000/orders/validate?id=1234568&valid=false
@orders.route('/orders/validate', methods=['GET', 'POST'])
@login_required
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
    
    if session._id != user : return permission_denied_return
    
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

#######################################################################################################################
#######################################################################################################################


# test url: http://127.0.0.1:5000/orders/finish?user=947426443@qq.com&id=1234568
@orders.route('/orders/finish', methods=['GET', 'POST'])
@login_required
def set_order_done():
    """
    Provides the operation for fnishing the orders.
    user: str.
    id: str.
    """
    data = select_data_source()
    user = data['user']
    order_id = data['id']
    
    if session._id != user  : return permission_denied_return
    
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

#######################################################################################################################
#######################################################################################################################

# test url: http://127.0.0.1:5000/orders/house_ranking?id=1234568&ranking=8
@orders.route('/orders/house_ranking', methods=['GET', 'POST'])
@login_required
def set_ranking_house():
    """
    Set the ranking to house.
    """
    data = select_data_source()
    order_id = data['id']
    ranking = float(data['ranking']) # TODO.
    user = session._id
    
    db = database.getdb()
    
    cmd = 'select customer from users where id=="{0}"'.format(order_id)
    customer_id_data = db.execute(cmd).fetchall()
    
    if len(customer_id_data) :
        return ranking_not_exist_return
    
    if customer_id_data[0][0] != user :
        return ranking_not_relative_return
    
    cmd = 'select house_ranked from orders where id=="{0}"'.format(order_id)
    ranked = db.execute(cmd).fetchall()[0][0]
    if ranked != 0 :
        return ranking_already_ranked_return
    
    cmd = 'select house from orders where id=="{0}"'.format(order_id)
    house_id = db.execute(cmd).fetchall()[0][0]
    
    cmd = 'select rank, rank_time from houses where id=="{0}"'.format(house_id)
    rank, rank_time = db.execute(cmd).fetchall()[0]
    
    rank = (rank * rank_time + ranking) / (rank_time + 1)
    rank_time += 1
    
    cmd = 'update houses set rank={0}, rank_time={1} where id="{0}"'.format(rank, rank_time, house_id)
    db.execute(cmd)
    db.commit()
    
    return ranking_complete_return

#######################################################################################################################
#######################################################################################################################

# test url: http://127.0.0.1:5000/orders/ranking?id=1234568&from=947426443@qq.com&to=1017002343@qq.com&ranking=8
@orders.route('/orders/ranking', methods=['GET', 'POST'])
@login_required
def set_ranking_users():
    """
    Set the ranking to users.
    Each user has one time.
    """
    data = select_data_source()
    order_id = data['id']
    from_user = data['from']
    to_user = data['to']
    ranking = float(data['ranking']) # TODO.
    
    if session._id != from_user and session._id != to_user : return permission_denied_return
    
    db = database.getdb()
    
    if not float.is_integer(ranking) or ranking <= 0 or 10 < ranking :
        return ranking_invalid_value_return
    
    ### Check if order exists.
    
    cmd = 'select * from orders where id=="{0}"'.format(order_id)
    order_info = db.execute(cmd).fetchall()
    if len(order_info) == 0 :
        return ranking_not_exist_return
    
    ### Check if user is valid.
    cmd = 'select owner, customer from orders where id=="{0}"'.format(order_id)
    owner, customer = db.execute(cmd).fetchall()[0]
    
    ### Check and setup ranked info in orders.
    
    if from_user == owner and to_user == customer :
        cmd = 'select owner_ranked from orders where id=="{0}"'.format(order_id)
        is_ranked = db.execute(cmd).fetchall()[0][0]
        if is_ranked != 0 :
            return ranking_already_ranked_return
        cmd = 'update orders set owner_ranked=1'
        db.execute(cmd)
        db.commit()
    elif from_user == customer and to_user == owner :
        cmd = 'select customer_ranked from orders where id=="{0}"'.format(order_id)
        is_ranked = db.execute(cmd).fetchall()[0][0]
        if is_ranked != 0 :
            return ranking_already_ranked_return
        cmd = 'update orders set customer_ranked=1'
        db.execute(cmd)
        db.commit()
    else :
        return ranking_not_relative_return
    
    ### Update rank to to_user.
    
    cmd = 'select rank, rank_time from users where mail=="{0}"'.format(to_user)
    rank, rank_time = db.execute(cmd).fetchall()[0]
    
    rank = (rank * rank_time + ranking) / (rank_time + 1)
    rank_time += 1
    
    cmd = 'update users set rank={0}, rank_time={1} where mail="{2}"'.format(rank, rank_time, to_user)
    db.execute(cmd)
    db.commit()    
    