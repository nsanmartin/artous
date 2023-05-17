import os

DEVSKEY = 'HWdojxqt5CwTmZuRhe9PigYcU0I'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or DEVSKEY

