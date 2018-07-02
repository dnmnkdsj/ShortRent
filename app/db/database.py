## Database.

from flask import g
from sqlite3 import *

def getdb():
    if not hasattr(g, 'database'):
        g.database = connect("all.db") # hard code database path.
    return g.database

db_create_users_cmd = 'create table if not exists users(' + ','.join([
    'mail TEXT primary key not null unique',
    'name TEXT not null',
    'password TEXT not null',
    'rankTimes INTEGER not null',
    'rank DOUBLE not null',
    'valid BOOL not null'
    ]) + ')'

db_create_houses_cmd = 'create table if not exists houses(' + ','.join([
    'id TEXT primary key not null unique',
    'address TEXT not null',
    'title TEXT  not null',
    'description TEXT not null',
    'master TEXT not null',
    'rank DOUBLE not null',
    'picture TEXT not null',
    'value DOUBLE not null',
    'valid BOOL not null'
    ]) + ')'

db_create_orders_cmd = 'create table if not exists orders(' + ','.join([
    'id TEXT primary key not null unique',
    'time TEXT not null',
    'value DOUBLE not null',
    'customer TEXT not null',
    'owner TEXT not null',
    'house TEXT not null',
    'passed BOOL not null',
    'done BOOL not null'
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
