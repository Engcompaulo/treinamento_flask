from itertools import count
from typing import Optional, List
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Treinamento do Paulo')
spec.register(server)
database = TinyDB('database.json')
c = count()


class Pessoa(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
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
    """Altera uma Pessoa a partir do ID no banco de dados."""
    Pessoa = Query()
    body = request.context.body.dict()
    database.update(body, Pessoa.id == id)
    return jsonify(body)

@server.delete('/pessoas/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def deleta_pessoa(id):
    """Remove uma pessoas a partir do ID do banco de dados."""
    Pessoa = Query()
    database.remove(Pessoa.id == id)
    return jsonify({})

server.run()
