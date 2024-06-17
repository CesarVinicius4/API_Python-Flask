from flask import Blueprint

# tem a mesma função do main, porém, fazemos isso de forma modularizada
# o que significa que podemos reutilizar esse código
bp = Blueprint('main', __name__)

# encapsulando as rotas de cliente
from app.routes import clients