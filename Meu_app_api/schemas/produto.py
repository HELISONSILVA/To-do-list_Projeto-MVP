from pydantic import BaseModel
from typing import List
from datetime import datetime
from model.produto import Produto
from schemas import ComentarioSchema


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado """
    nome: str         # ✅ SEM DEFAULT!
    urgencia: str     # ✅ SEM DEFAULT!
    data: datetime    # ✅ SEM DEFAULT!


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. """
    nome: str


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada. """
    produtos: List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação dos produtos seguindo o schema definido em ProdutoViewSchema. """
    result = []
    for produto in produtos:
        result.append({
            "nome": produto.nome,
            "urgencia": produto.urgencia,
            "data": produto.data.isoformat()
        })
    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários. """
    id: int
    nome: str
    urgencia: str
    data: datetime
    total_comentarios: int
    comentarios: List[ComentarioSchema]


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    message: str
    nome: str


def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em ProdutoViewSchema. """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "urgencia": produto.urgencia,
        "data": produto.data.isoformat(),
        "total_comentarios": len(produto.comentarios),
        "comentarios": [{"texto": c.texto} for c in produto.comentarios]
    }
