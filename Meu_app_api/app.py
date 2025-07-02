from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

from model import Session, Produto, Comentario
from logger import logger
from schemas import *

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para a documentação
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário a um produto cadastrado")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para a tela de documentação /openapi"""
    return redirect('/openapi')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(body: ProdutoSchema):  # ✅ AGORA É body, não form!
    """Adiciona um novo Produto à base de dados"""
    produto = Produto(
        nome=body.nome,
        urgencia=body.urgencia,
        data=body.data
    )
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    session = Session()
    try:
        session.add(produto)
        session.commit()
        logger.debug(f"Produto '{produto.nome}' adicionado com sucesso")
        return apresenta_produto(produto), 200
    except IntegrityError:
        session.rollback()
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}': {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        session.rollback()
        error_msg = f"Não foi possível salvar novo item :/ ({e})"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}': {error_msg}")
        return {"message": error_msg}, 400
    finally:
        session.close()


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Busca todos os produtos cadastrados"""
    session = Session()
    try:
        produtos = session.query(Produto).all()
        if not produtos:
            return {"produtos": []}, 200
        else:
            logger.debug(f"{len(produtos)} produtos encontrados")
            return apresenta_produtos(produtos), 200
    finally:
        session.close()


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Busca um produto pelo nome"""
    produto_nome = query.nome
    session = Session()
    try:
        produto = session.query(Produto).filter(Produto.nome == produto_nome).first()
        if not produto:
            error_msg = "Produto não encontrado na base :/"
            logger.warning(f"Erro ao buscar produto '{produto_nome}': {error_msg}")
            return {"message": error_msg}, 404
        logger.debug(f"Produto encontrado: '{produto.nome}'")
        return apresenta_produto(produto), 200
    finally:
        session.close()


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um produto pelo nome"""
    produto_nome = unquote(unquote(query.nome))
    session = Session()
    try:
        count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
        session.commit()
        if count:
            logger.debug(f"Produto '{produto_nome}' deletado")
            return {"message": "Produto removido", "id": produto_nome}, 200
        else:
            error_msg = "Produto não encontrado na base :/"
            logger.warning(f"Erro ao deletar produto '{produto_nome}': {error_msg}")
            return {"message": error_msg}, 404
    finally:
        session.close()


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def add_comentario(body: ComentarioSchema):  # ✅ Também usa body
    """Adiciona um comentário a um produto"""
    produto_id = body.produto_id
    session = Session()
    try:
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            error_msg = "Produto não encontrado na base :/"
            logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}': {error_msg}")
            return {"message": error_msg}, 404

        comentario = Comentario(body.texto)
        produto.adiciona_comentario(comentario)
        session.commit()
        logger.debug(f"Comentário adicionado ao produto #{produto_id}")
        return apresenta_produto(produto), 200
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
