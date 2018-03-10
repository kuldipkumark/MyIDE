import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MyIDE_secret_key'

    CLIENT_ID = os.environ.get('CLIENT_ID') or '19e83f4b909394d4387535acce0cb16a403985a01f7d.api.hackerearth.com'
    CLIENT_SECRET_KEY = os.environ.get('CLIENT_SECRET_KEY') or '4acde50b23e29070bad8ed489b4dcffc488b6169'
    COMPILE_URL = os.environ.get('COMPILE_URL') or 'http://api.hackerearth.com/code/compile/'
    RUN_URL = os.environ.get('RUN_URL') or 'http://api.hackerearth.com/code/run/'


    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False