from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from app.db import db
from app.auth import token_required, auth_bp

# responsável por fazer a migração no banco, manter histórico e automatizar o processo
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    # configuração será de acordo com o arquivo de configuração
    app.config.from_object(config_class)

    app.config['SECRET_KEY'] = 'your-secret-key'

    #inicializa o banco de dados
    db.init_app(app)
    migrate.init_app(app, db)

    # o blueprint de todas as rotas é o blueprint criado
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # definindo a url de autenticação
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # tratamento de mensagens de erro
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'Internal server error'}), 500

    @app.errorhandler(503)
    def server_unavailable(error):
        return jsonify({'message': 'Server unavailable'}), 503

    return app