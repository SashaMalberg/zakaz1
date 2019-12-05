import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    POSTGRES_URL = "localhost:5432"
    POSTGRES_USER = "postgres"
    POSTGRES_PW = "root"
    POSTGRES_DB = "test"
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                                   db=POSTGRES_DB)
