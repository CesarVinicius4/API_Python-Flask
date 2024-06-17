import os

# Caminho relativo da sua aplicação
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # url de conexão com o banco de dados
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # utilizado para controle de modificações no banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False