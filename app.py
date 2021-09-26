from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Treinamento do Paulo')
spec.register(server)

class Pessoa(BaseModel):
    id: int
    nome: str
    idade: int

@server.get('/cadastros')
@spec.validate(resp=Response(HTTP_200=Pessoa))
def pegar_cadastros():
    return "Felipe Luiz"

@server.post('/cadastros')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def inserir_cadastro():
    """Insere um novo cadastro no banco de dados."""
    body = request.context.body.dict()
    return body
    ...


server.run()
