# Test for database.

from flask import redirect, current_app, g

from . import inner_test
from ..db import database

@current_app.route('/test/database')
def test_database():
    """
    Sample: Opeartions on database.
    """
    # this is not necessary.
    # tables can be created manually.
    # or this can be put into initializing.
    database.ensure_tables_exist()
    
    # use this to get database for better performance.
    db = database.getdb()
    
    # Do anything you want...
    db.execute('insert into test_users values("xxx", 124)')
    
    # Do *NOT* forget this...
    # or the command will not be executed..
    db.commit()
    
    return redirect('/test/page')

@current_app.teardown_appcontext
def close_db(err):
        database.detachdb()