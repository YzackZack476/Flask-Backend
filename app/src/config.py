from distutils.debug import DEBUG


class DevelopmentConfig():
    DEBUG = True
# Parametros para la base de datos
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASS = 'Issac#corona'
    MYSQL_DB = 'test'

config = {
    'development': DevelopmentConfig
}