from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Treinamento do Paulo')
spec.register(server)

@server.get('/cadastros')
def pegar_cadastros():
    return "Felipe Luiz"

server.run()
