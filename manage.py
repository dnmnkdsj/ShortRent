#!/usr/bin/env python3
import os
from app import create_app
from flask_script import Manager

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
