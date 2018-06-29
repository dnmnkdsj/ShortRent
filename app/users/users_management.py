from . import users
from ..db import database

# an example.
# remove it when you begin developing and see this bad...
@users.route("/test/users")
def users_test():
    return 'Hello users!'