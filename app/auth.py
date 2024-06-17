import datetime
import jwt

# utilizado para encapsular os métodos dentro de uma outra função
from functools import wraps

from flask import request, jsonify, Blueprint, current_app

auth_bp = Blueprint('auth', __name__)

#criando o login
@auth_bp.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json() # o Blueprint já garante que vai vir um json
    username = auth_data.get('username')
    password = auth_data.get('password')

    # verifica se existe no banco, porém, vamos fazer no modo fácil

    if username == 'admin' and password == 'password':
        # se entrou, o usuário foi autenticado
        token = jwt.encode(
            {
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                # minimo de informação necessário
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'token': token}), 200 # status ok
    return jsonify({'message': 'Invalid username or password'}), 401 # erro de autenticação

# criar a marcação de rotas. Essa função vai ser encapsulada com o método decorated
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # De agora em diante , sempre vai buscar o token no header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401 # erro de autenticação

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user'] # usado nas rotas
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401 # erro de autenticação
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401 # erro de autenticação
        # passa os argumentos recebidos para a função seguinte
        return f(current_user, *args, **kwargs)
    return decorated