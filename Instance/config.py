import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_pass_code_hard_to_crack'
    PAGE_USERS = 3
    PAGE_PRODUCTS = 7
    PAGE_ITEMS = 10

class TestingConfig(Config):
    DEBUG  = True