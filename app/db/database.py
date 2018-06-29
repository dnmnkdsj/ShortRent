## Database.

from flask import g
from sqlite3 import *

def getdb():
    if not hasattr(g, 'database'):
        g.database = connect("all.db") # hard code database path.
    return g.database

db_create_users_cmd = 'create table if not exists users(' + ','.join([
    'mail text primary key',
    'name text',
    'password text',
    'rank real',
    'valid bit'
    ]) + ')'

db_create_houses_cmd = 'create table if not exists hosues(' + ','.join([
    'id text primary key',
    'address text',
    'title text',
    'description text',
    'master text',
    'rank real',
    'picture text',
    'orders text',
    'value real',
    'valid bit'
    ]) + ')'
db_create_orders_cmd = 'create table if not exists orders(' + ','.join([
    'id text primary key',
    'time text',
    'value real',
    'customer text',
    'owner text',
    'passed bit',
    'state bit'
    ]) + ')'

def ensure_tables_exist():
    global db_create_users_cmd, db_create_houses_cmd, db_create_orders_cmd
    """
    Create tables if tables does not exist.
    All table values are hard-coded here.
    Since all database operation uses this module this shouldn't be an issue...
    """
    db = getdb()
    db.execute(db_create_users_cmd)
    db.execute(db_create_houses_cmd)
    db.execute(db_create_orders_cmd)

def detachdb():
    if hasattr(g, 'database'):
        db = g.database
        db.close()
