import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "i_am_the_biggest_and_the_baddest"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

configuration = {
    'default': Config,
    'testing': TestingConfig
}