# This file provide funtions to routing to ordering pages.

from flask import session
from . import orders
from .utils import *
from time import *
from flask_login import login_required

orders_creation_page = redirect('/test/page')

create_complete_return = jsonify([0, 'Done.'])
create_invalid_value_return = jsonify([1, 'Value cannot be less than 0.'])
create_house_not_found_return = jsonify([2, 'House does not exist.'])
create_self_dealing_return = jsonify([3, 'Dealing with yourself is prevented.'])
create_conflict_return = jsonify([4, 'An order using this house at this time is already confirmed.'])

# for creating new orders.
@orders.route('/orders/new')
def get_orders_creating_page():
    return orders_creation_page

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
@login_required
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
    
    ### User permision check.
    
    if check_user_permission(user) : return permission_denied_return
    
    ### Value validate check.
    
    if int(value) < 0 :
        return create_invalid_value_return
    
    ### House existion check.
    
    cmd = 'select * from houses where id=="{0}"'.format(house)
    house_info = db.execute(cmd).fetchall()
    if len(house_info) == 0 :
        return create_house_not_found_return
    
    ### House master and user comparation check.
    
    cmd = 'select master from houses where id=="{0}"'.format(house)
    house_master = db.execute(cmd).fetchall()[0][0]
    if user == house_master :
        return create_self_dealing_return
    
    ### Conflict time check.
    
    cmd = 'select * from orders where house=="{0}" AND time=="{1}" AND passed==1'.format(house, time)
    print('conflict: ', cmd)
    orders_conflict = db.execute(cmd).fetchall()
    if len(orders_conflict) != 0 :
        return create_conflict_return
    
    ### Check finished.
    ### Do the operation.
    
    cmd = 'insert into orders values (' + ','.join([
        '"{0}"'.format(create_id()),        # id
        '"{0}"'.format(time),               # time
        '{0}'.format(value),                # value
        '"{0}"'.format(user),               # customer
        '"{0}"'.format(house_master),       # owner
        '0',
        '0',
        '0',
        '"{0}"'.format(house),              # house
        '0',                                # passed
        '0'                                 # done
        ]) + ')'
    db.execute(cmd)
    db.commit()
    
    print('order confirmed: cutomer: {} owner: {} time: {}'.format(user, house_master, time))
        
    return create_complete_return
