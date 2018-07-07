import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Secret key"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'just a key'

    JSONIFY_PRETTYPRINT_REGULAR = False

    '''don't know what this is'''
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Mail server settings
    """
    MAIL_SERVER = 'smtp.126.com',
    MAIL_PORT = 465,  # this port number should be 465 which is encoded, not what 163.com says 25.
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'hydroxyapatite@126.com',
    MAIL_PASSWORD = 'hyperoxygen0',
    MAIL_SENDER = 'hydroxyapatite@126.com',
    MAIL_DEFAULT_SENDER = 'hydroxyapatite@126.com'
    """Debug setting"""
    DEBUG = True


<<<<<<< HEAD
config = {
    'development': DevelopmentConfig,
=======

class ReleaseConfig(Config):
    """
    Mail server settings
    """
    MAIL_SERVER = 'smtp.126.com',
    MAIL_PORT = 465,  # this port number should be 465 which is encoded, not what 163.com says 25.
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'hydroxyapatite@126.com',
    MAIL_PASSWORD = 'hyperoxygen0',
    MAIL_SENDER = 'hydroxyapatite@126.com',
    MAIL_DEFAULT_SENDER = 'hydroxyapatite@126.com'
    """Debug setting"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'release': ReleaseConfig,
>>>>>>> 3d3f9a4df9ce0beceb2b4b2931e0c6b8130279d1
    'default': DevelopmentConfig
}