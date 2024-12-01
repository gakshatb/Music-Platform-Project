class appconfig:
    SECRET_KEY = '123'


class dataconfig:
    database = 'database.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False