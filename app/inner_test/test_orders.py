from . import inner_test
from flask import current_app

@inner_test.route('/test/orders')
def test_orders():
    with current_app.test_request_context('/orders/getinfo'):
        pass