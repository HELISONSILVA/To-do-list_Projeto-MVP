# 📌 Minha API — Projeto MVP Full Stack 🚀

Este é o **primeiro projeto de API** desenvolvido como parte da trilha do **curso de Desenvolvimento Full Stack** da **PUC Rio**.  
Ele utiliza **Flask**, **SQLAlchemy**, **Pydantic** e **Flask OpenAPI3** para expor uma API RESTful simples com **documentação interativa**.

## ✅ Requisitos

- **Python 3.8 ou superior**
- **Pip** atualizado
- Recomenda-se usar **ambiente virtual** ([virtualenv](https://virtualenv.pypa.io/en/latest/installation.html))

## ⚙️ Instalação das dependências

1️⃣ Clone o repositorio no Github

2️⃣ Acesse o diretório raiz do projeto:

cd “Meu_app_api”

3️⃣ Crie e ative um **ambiente virtual**:

**Linux/MacOS**

python3 -m venv env
source env/bin/activate

**Windows**

python -m venv env
env\Scripts\activate

4️⃣ Instale todas as dependências:

(env) $ pip install -r requirements.txt


## ▶️ Como executar a API

No terminal, dentro da pasta onde está o arquivo `app.py`:
(env) $ flask run --host 0.0.0.0 --port 5000

**Exemplo Windows:**

(env) $ cd "C:\Users\Helis\Downloads\Projeto MVP\Meu_app_api"
(env) $ flask run --host 0.0.0.0 --port 5000

## 🔄 Modo desenvolvimento com auto-reload

Para reiniciar automaticamente ao salvar alterações no código, use o `--reload`:

(env) $ flask run --host 0.0.0.0 --port 5000 --reload


## 🌐 Acessar a documentação da API

Assim que o servidor estiver rodando, abra seu navegador em:

[http://localhost:5000](http://localhost:5000)

Você será **redirecionado automaticamente** para a página `/openapi`, onde verá a interface interativa da API:
- **Swagger UI**
- **Redoc**
- **RapiDoc**

Nela você pode:
✅ Ver todos os endpoints disponíveis  
✅ Fazer chamadas `GET`, `POST` e `DELETE` direto pelo navegador  
✅ Testar a API sem precisar de Postman


## 🗂️ Notas importantes

- **Banco de dados:** utiliza SQLite local (`/database/db.sqlite3`).
- Para **resetar o banco**, basta apagar o arquivo `.sqlite3` e reiniciar a aplicação.
- **Produção:** Para uso real, troque SQLite por PostgreSQL, MySQL ou outro banco robusto.
- O projeto foi desenvolvido para **estudo**, mas segue boas práticas de API REST com **validação de dados**, **logs** e **documentação automática**
