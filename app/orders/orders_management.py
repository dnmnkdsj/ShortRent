# this module is only for administrators' management.

from . import orders
from flask import session, current_app, jsonify
from ..db import database

def check_permission():
    # TODO: enable session.
    # if 'admin' not in session:
    #   return False
    return True

@orders.route("/orders/all")
def get_all_orders():
    if not check_permission(): return "PERMISSION DENIED"
    db = database.getdb()
    cmd = 'select * from test_users'
    data = db.execute(cmd).fetchall()
    return jsonify(data)
