import os
import logging
from flask import Flask, jsonify, request
from flask_jwt_extended import  create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_cors import CORS
from flasgger import Swagger, swag_from
from datetime import datetime, timedelta
from src.chat import Chat 
from src.logger import setup_logging
from src.message import Mensagem
from src.exceptions import AuthError, ChatError, DatabaseError

setup_logging()
log = logging.getLogger(__name__)

app = Flask(__name__)

secret = os.getenv('JWT_SECRET_KEY')
if not secret:
    raise ValueError("[DANGER]: CHAVE JWT INEXISTENTE!")
app.config["JWT_SECRET_KEY"] = secret
app.config["JWT_ACCESS_TOKEN"] = timedelta(minutes=60)
app.config["PROPAGATE_EXCEPTIONS"] = True

CORS(app, resources={
    r"/*": {
        "origins": os.getenv("ALLOWED_ORIGINS", "*").split(","),
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }

swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "ChatAWS API",
            "description": "API de chat com autenticação JWT",
            "version": "1.0.0",
            "contact": {
                "name": "Mista",
                "email": "mista.ayo7@gmail.com"
                }
            },
        "securityDefinitions":{
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Token JWT no formato: Bearer {token}"
            }
        },
        "schemes": ["http", "https"],
        "tags": [
            {"name": "Autenticação","description": "Endpoints de registro e login"},
            {"name": "Mensagens","description": "Enpoints de envio e busca de mensagens"},
            {"name": "Sistema","description": "Enpoints de envio e busca de mensagens"}
        ]
    } 

swagger = Swagger(app, config=swagger_config, template=swagger_template)

jwt = JWTManager(app)

try:
    chat_app = Chat()
    log.info("Instancia do Chat criada com sucesso")

except ChatError as e:
    log.critical("[ERRO] Falha fatal ao instanciar o Chat: %s", e)
    chat_app = None

def success_response(message, data=None, status_code=200):
    """Rrtorna uma resposta de sucesso padrão"""
    response = {"success": True, "message": message}
    if data:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message, status_code=400):
    """Retorna uma resposta de erro padrão"""
    return jsonify({
        "success": False,
        "error": message
        }), status_code

@app.errorhandler(404)
def not_found(error):
    """Endpoint não encontrado"""
    return error_response("Endpoint não encontrado", 404)

@app.errorhandler(500)
def internal_error(error):
    """Erro interno do servidor"""
    return error_response("Erro interno do servidor", 500)

@jwt.expired_token_loader
def expired_token_callback(error):
    """Token JWT expirado"""
    return error_response("Token JWT expirado", 401)

@jwt.invalid_token_loader
def invalid_token_callback(eror):
    """Token JWT inválido"""
    return error_response("Token JWT inválido")

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Token JWT inexistente"""
    return error_response("Token não autorizado")

@app.route("/", methods=["GET"])
def index():
    """
    Página inicial da API
    """
    return success_response(
        "ChatAWS API v1.0",
        data={
            "version": "1.0.0",
            "documentation": "/docs",
            "health": "/health",
            "endpoints": {
                "auth": ["/auth/register", "/auth/login", "/auth/me"],
                "messages": ["/messages/post", "/messages/all", "/messages/search"]
            }
        }
    )

@app.route("/auth/register", methods=["POST"])
def register():
    """
    Endpoint para registrar um novo usuário.
    """
    if not chat_app:
        return error_response("Servidor não inicalizado", 500)

    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    email = dados.get('email')

    try:
        chat_app.auth.registrar(usuario, senha, email)
        log.info("O usuario %s foi resgistrado via API", usuario)
        return success_response("Usuário registrado com sucesso", status_code=201)

    except (AuthError, DatabaseError) as e:
        log.warning("Falha no registro do usuário %s: %s", usuario, e)
        return error_response(str(e), 400)

@app.route("/health", methods=["GET"])
def health():
    """Endpoint que checa se a API está operacional"""
    health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "database": "connected" if chat_app else "error"
    }
    status_code = 200 if chat_app else "error"
    return success_response("API operacional", data=health_status, status_code=status_code)
    
@app.route("/auth/login", methods=["POST"])
def login():
    """
    Endpoint para logar e obter o token JWT.
    """
    if not chat_app:
        return error_response("Servidor não inicializado", 500)

    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    
    try: 
        user_id = chat_app.auth.login(usuario, senha)
        access_token = create_access_token(identity=str(user_id))
        log.info("Login efetuado pelo usuário %s", usuario)
        return success_response(
                "Login realizado com sucesso",
                data={"token": access_token},
                status_code=200
        )

    except (AuthError, DatabaseError) as e:
        log.warning("[ERRO] Faha no login do usuario %s: %s", usuario, e)
        return error_response(str(e), 401)

@app.route("/auth/me", methods=["GET"])
@jwt_required()
def get_me():
    """
    Endpoint para buscar as informções do usuário
    """
    try:
        user_id_logado = get_jwt_identity()
        info = chat_app.auth.exibir_info_usuario(user_id_logado)

        if info:
            return success_response("infomações obtidas com sucesso",
                    data=info,
                    status_code=200
            )
        else:
            return error_response("O usuário não foi encontrado", 404)

    except DatabaseError as e:
        log.error("Erro no Banco de dados ao buscar as informaçoes do usuário: %s", e)
        traceback.print_exc()
        return error_response(str(e), 500)
        
@app.route("/messages/post", methods=["POST"])
@jwt_required()
def post_message():
    """
    Endpoint para o envio de mensagens do usuário
    """
    user_id_logado = get_jwt_identity()
    dados =  request.json
    conteudo = dados.get('conteudo')

    try: 
        chat_app.enviar_mensagem(user_id_logado, conteudo)
        log.info("Mensagem recebida via API pelo id %s: ", user_id_logado)
        return success_response("Mensagem enviada com sucesso", status_code=201)

    except (ChatError, DatabaseError) as e:
        info.warning("[Erro] Falha no envio da mensagem id: %s: %s", user_id_logado, e)
        return error_response(str(e), 400)

@app.route("/messages/all", methods=["GET"])
def get_messages():
    """
    Endpoint para listar todas as mensagens.
    """
    try:
        mensagens = chat_app.carregar_mensagens()
        mensagens_formatadas = [msg.formatar() for msg in mensagens]

        return success_response(
            "Mensages listadas com sucesso",
            data=mensagens_formatadas,
            status_code=200
        )
    except DatabaseError as e:
        log.error("[Erro] Falha ao listar as mensagens do banco de dados", e)
        return error_response(str(e), 500)

@app.route("/messages/search", methods=["GET"])
@jwt_required()
def get_messages_user():
    """
    Endpoint para listar as ultimas 20 mensagens baseado na busca pelo usuário.
    """
    usuario_busca = request.args.get('usuario')
    if not usuario_busca:
        return error_response("Parametro 'usuario' não encontrado", 400)
    try:
        lista_mensagens = chat_app.buscar_mensagens_usuario(usuario_busca)
        mensagens_formatadas = []
        for dados_msg in lista_mensagens:
            id_msg, usuario, mensagem, data_str = dados_msg
            timestamp = datetime.fromisoformat(data_str)
            msg = Mensagem(usuario, mensagem, id_msg, timestamp)
            mensagens_formatadas.append(msg.formatar())
        return success_response(
                f"Mensagens de '{usuario_busca}' encontradas",
                data=mensagens_formatadas,
                status_code=200
        )
    except (ChatError, DatabaseError) as e:
        log.error("[Erro] Falha ao listar as mensagens do banco de dados: %s", e)
        return error_response(str(e), 400)
    except Exception as e:
        log.error("[Erro] Fatal no endpoint de busca: %s", e)
        return error_response(str(e), 500)

if __name__ == "__main__":
    ambiente = os.getenv("FLASK_ENV", "development")
    debug = ambiente == "development"
    if not debug:
        print("\n" + "="*70)
        print("ChatAWS API rodando em PRODUÇÃO")
        print("Documentação: http://localhost:5000/docs")
        print("Health Check: http://localhost:5000/health")
        print("="*70 + "\n")

    log.info("Iniciando o servidor...")
    app.run(host="0.0.0.0", debug=debug, port=5000)
