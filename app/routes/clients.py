from flask import jsonify, request, abort
from app import db
from app.models import Client
from app.routes import bp
from app.auth import token_required

@bp.route('/clients', methods=['GET'])
@token_required
def get_client(current_user):
    # recupera um parâmetro passado na chamada da rota
    client_id = request.args.get('client_id')

    if client_id:
        try:
            client = Client.query.get_or_404(client_id)
            # se encontrou o cliente, retorna ele
            return jsonify(client.to_dict())
        except Exception as e:
            return jsonify({'error': str(e)}), 500 # Erro de servidor
    else:
        try:
            clients = Client.query.all()
            return jsonify([client.to_dict() for client in clients])
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Erro de servidor

# rota para criar cliente
@bp.route('/clients', methods=['POST'])
@token_required
def create_client(current_user):
    try:
        data = request.get_json() or {} # ou vamos um json para ler ou aceita o que vier

        # começa as verificações
        if 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Username and Email are required.'}), 400 # bad request
        if Client.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username is already registered'}), 400 # bad request
        if Client.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email is already registered'}), 400 # bad request

        # caso não caiu em nenhum if, está tudo certo
        client = Client(username=data['username'], email=data['email'])
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict()), 201 # sucesso ao criar cliente
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # erro de servidor

# Exemplo de PUT
@bp.route('/clients/<int:id>', methods=['PUT'])
@token_required
def update_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        data = request.get_json() or {}

        if 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Name and Email are required'}), 404 # bad request
        if Client.query.filter_by(username=data['username']).first(): # se já existir o nome, retorna o erro
            return jsonify({'error': 'Name already registered'}), 400
        if Client.query.filter_by(email=data['email']).first(): # se já existir o email, retorna o erro
            return jsonify({'error' : 'Email is already registered'}), 400

        client.username = data['username']
        client.email = data['email']
        db.session.commit()
        return jsonify(client.to_dict()), 200 # sucesso na atualização
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # erro de servidor

# Exemplo de DELETE
@bp.route('/clients/<int:id>', methods=['DELETE'])
@token_required
def delete_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Cliente deletado com sucesso'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500