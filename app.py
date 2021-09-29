from itertools import count
from typing import Optional, List
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Treinamento do Paulo')
spec.register(server)
#database = TinyDB('database.json') Com essa linha, o banco não é sobreescrito
database = TinyDB(storage=MemoryStorage) # Toda hora que a aplicação reinicia, o banco zera
c = count()

class QueryPessoa(BaseModel):
    id: Optional[int] 
    nome:  Optional[str]
    idade:  Optional[int]


class Pessoa(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    nome: str
    idade: int

class Pessoas(BaseModel):
    pessoas: List[Pessoa]
    count: int


@server.get('/pessoas')
@spec.validate(
    query=QueryPessoa,
    resp=Response(HTTP_200=Pessoas)
)
def buscar_pessoas():
    """Retorna todas as Pessoas da base de dados."""
    query = request.context.query.dict(exclude_none=True)
    todas_as_pessoas = database.search(
        Query().fragment(query)
    )
    return jsonify(
        Pessoas(
            #pessoas=database.all(),
            pessoas=todas_as_pessoas,
            count=len(todas_as_pessoas)
        ).dict()
    )


@server.get('/pessoas/<int:id>')
@spec.validate(resp=Response(HTTP_200=Pessoa))
def buscar_pessoa(id):
    """Retorna uma Pessoas da base de dados pelo ID."""
    try:
        pessoa = database.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Pessoa não encontrada!'}, 404
    return jsonify(pessoa)


@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_201=Pessoa))
def inserir_pessoa():
    """Insere uma nova pessoa no banco de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body
    ...

@server.put('/pessoas/<int:id>')
@spec.validate(
    body=Request(Pessoa), resp=Response(HTTP_201=Pessoa)
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
