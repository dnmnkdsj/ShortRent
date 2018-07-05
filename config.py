import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Secret key"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'just a key'

    '''don't know what this is'''
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Mail server settings
    """
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'hx763479239@163.com'
    MAIL_PASSWORD = 'hx763479239hx1'
    """Debug setting"""
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}