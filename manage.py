#!/usr/bin/env python3
import os
from app import create_app
from flask_script import Manager

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'
if __name__ == '__main__':
    manager.run()
