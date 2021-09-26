from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Treinamento do Paulo')
spec.register(server)
database = TinyDB('database.json')

class Pessoa(BaseModel):
    id: int
    nome: str
    idade: int

@server.get('/cadastros')
def pegar_cadastros():
    """Retorna todas os cadastros da base de dados. """
    return jsonify(database.all())


@server.post('/cadastros')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def inserir_cadastro():
    """Insere um novo cadastro no banco de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body
    ...


server.run()
