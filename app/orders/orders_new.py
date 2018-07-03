# This file provide funtions to routing to ordering pages.

from flask import session
from . import orders
from .utils import *
from time import *

# TODO:
# pages.
orders_creation_page = redirect('/test/page')

# TODO:
# returns.
invalid_user_return = jsonify('User does not exist or is invalid.')
invalid_value_return = jsonify('Value cannot be less than 0.')
conflict_return = jsonify('Time conflict.')
house_not_found_return = jsonify('house not found.')
self_dealing_return = jsonify('Self-buying not allowed.')
complete_return = jsonify('Done.')


# for creating new orders.
@orders.route('/orders/new')
def get_orders_creating_page():
    return orders_creation_page

@orders.route('/orders/newid')
def create_id():
    """
    Check the max id from orders table, and select a bigger integer.
    """
    db = database.getdb()
    # Notice there is a global write lock to the databse file,
    #    this command should run properly with reading access.
    cmd = 'select MAX(id) from orders'
    max_id = db.execute(cmd).fetchall()
    if len(max_id) == 0:
        max_id.append(('0', None))
    return str(int(max_id[0][0]) + 1)
    
# test url: http://127.0.0.1:5000/orders/create?user=947426443@qq.com&house=1017002344&value=1000&time=2018-9-26
@orders.route('/orders/create', methods=['GET', 'POST'])
def create_order():
    """
    The frontend submits a form to makeup the database.
    Parameter structure:
    user : string
    house : string
    value : string
    time : string 'yyyy-mm-dd'
    use argument form=true to enable form data delivering.
    """
    
    data = select_data_source()
    user = data['user']
    house = data['house']
    value = data['value']
    time = get_std_time_str(data['time'])
    
    db = database.getdb()
    
    ### User validation check.
    
    cmd = 'select * from users where mail=="{0}" AND valid!=0'.format(user)
    user_info = db.execute(cmd).fetchall()
    if len(user_info) == 0 :
        return invalid_user_return
    
    ### User permision check.
    
    if not check_user_permission(user) :
        return permission_denied_return
    
    ### Value validate check.
    
    if int(value) < 0 :
        return invalid_value_return
    
    ### House existion check.
    
    cmd = 'select * from houses where id=="{0}"'.format(house)
    house_info = db.execute(cmd).fetchall()
    if len(house_info) == 0 :
        return house_not_found_return
    
    ### House master and user comparation check.
    
    cmd = 'select master from houses where id=="{0}"'.format(house)
    house_master = db.execute(cmd).fetchall()[0][0]
    if user == house_master :
        return self_dealing_return
    
    ### Conflict time check.
    
    cmd = 'select * from orders where house=="{0}" AND time=="{1}"'.format(house, time)
    print('conflict: ', cmd)
    orders_conflict = db.execute(cmd).fetchall()
    if len(orders_conflict) != 0 :
        return conflict_return
    
    ### Check finished.
    ### Do the operation.
    
    cmd = 'insert into orders values (' + ','.join([
        '"{0}"'.format(create_id()),        # id
        '"{0}"'.format(time),               # time
        '{0}'.format(value),                # value
        '"{0}"'.format(user),               # customer
        '"{0}"'.format(house_master),       # owner
        '"{0}"'.format(house),              # house
        '0',                                # passed
        '0'                                 # done
        ]) + ')'
    db.execute(cmd)
    db.commit()
    
    print('order confirmed: cutomer: {} owner: {} time: {}'.format(user, house_master, time))
        
    return complete_return
