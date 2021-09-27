from typing import Optional, List
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Treinamento do Paulo')
spec.register(server)
database = TinyDB('database.json')

class Pessoa(BaseModel):
    id: Optional[int]
    nome: str
    idade: int

class Pessoas(BaseModel):
    pessoas: List[Pessoa]
    count: int


@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoas))
def buscar_pessoas():
    """Retorna todas as Pessoas da base de dados."""
    return jsonify(
        Pessoas(
            pessoas=database.all(),
            count=len(database.all())
        ).dict()
    )
#    return jsonify(database.all())


@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def inserir_pessoa():
    """Insere uma nova pessoa no banco de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body
    ...

@server.put('/pessoas/<int:id>')
@spec.validate(
    body=Request(Pessoa), resp=Response(HTTP_200=Pessoa)
)
def altera_pessoa(id):
    Pessoa = Query()
    body = request.context.body.dict()
    database.update(body, Pessoa.id == id)
    return jsonify(body)


server.run()
