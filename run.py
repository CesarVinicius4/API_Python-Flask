from app import create_app, db
from app.models import Client

# onde vamos criar o app
app = create_app()

# vamos usar apenas o contexto shell para rodar comandos
@app.shell_context_processor
def make_shell_context():
    # chaves que vão estar disponíveis no contexto shell
    return {'db': db, 'client': Client}