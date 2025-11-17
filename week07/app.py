import logging
from flask import Flask, jsonify, request
from flask_jwt_extended import  create_access_token, jwt_required, get_jwt_identity, JWTManager
from chat import Chat 
from logger import setup_logging
from message import Mensagem
from datetime import datetime
from exceptions import AuthError, ChatError, DatabaseError

setup_logging()
log = logging.getLogger(__name__)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "senha_secreta"
app.config["PROPAGATE_EXCEPTIONS"] = True
jwt = JWTManager(app)

try:
    chat_app = Chat()
    log.info("Instancia do Chat criada com sucesso")

except ChatError as e:
    log.critical("[ERRO] Falha fatal ao instanciar o Chat: %s", e)
    chat_app = None

@app.route("/auth/register", methods=["POST"])
def register():
    """
    Endpoint para registrar um novo usuário.
    """
    if not chat_app:
        return jsonify({"erro": "Servidor não inicalizado"}), 500

    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    email = dados.get('email')

    try:
        chat_app.auth.registrar(usuario, senha, email)
        log.info("O usuario %s foi resgistrado via API", usuario)
        return jsonify({"mensagem": "Usuário registrado com sucesso"}), 201

    except (AuthError, DatabaseError) as e:
        log.warnnig("Falha no registro do usuário %s: %s", usuario, e)
        return jsonify({"erro": str(e)}), 400

@app.route("/auth/login", methods=["POST"])
def login():
    """
    Endpoint para logar e obter o token JWT.
    """
    if not chat_app:
        return jsonify({"erro": "Servidor não inicializado"}), 500

    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    
    try: 
        user_id = chat_app.auth.login(usuario, senha)

        access_token = create_access_token(identity=str(user_id))

        log.info("Login efetuado pelo usuário %s", usuario)
        return jsonify(token=access_token), 200

    except (AuthError, DatabaseError) as e:
        log.warning("[ERRO] Faha no login do usuario %s: %s", usuario, e)
        return jsonify({"erro": str(e)}), 401

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
            return jsonify(info), 200
        else:
            return jsonify({"erro": "O usuário não foi encontrado"}), 404

    except DatabaseError as e:
        log.error("Erro no Banco de dados ao buscar as informaçoes do usuário", e)
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 500
        
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
        return jsonify({"mensagem": "Mensagem enviada com sucesso"}), 201

    except (ChatError, DatabaseError) as e:
        info.warning("[Erro] Falha no envio da mensagem id: %s: %s", user_id_logado, e)
        return jsonify({"erro": str(e)}), 400

@app.route("/messages/all", methods=["GET"])
def get_messages():
    """
    Endpoint para listar todas as mensagens.
    """
    try:
        mensagens = chat_app.carregar_mensagens()
        mensagens_formatada = [msg.formatar() for msg in mensagens]

        return jsonify(mensagens_formatada), 200
    except DatabaseError as e:
        log.error("[Erro] Falha ao listar as mensagens do banco de dados", e)
        return jsonify({"erro": str(e)}), 500

@app.route("/messages/search", methods=["GET"])
@jwt_required()
def get_messages_user():
    """
    Endpoint para listar as ultimas 20 mensagens baseado na busca pelo usuário.
    """
    usuario_busca = request.args.get('usuario')
    if not usuario_busca:
        return jsonify({"erro": "Parametro 'usuario' não encontrado"}), 400
    try:
        lista_mensagens = chat_app.buscar_mensagens_usuario(usuario_busca)
        mensagens_formatadas = []
        for dados_msg in lista_mensagens:
            id_msg, usuario, mensagem, data_str = dados_msg
            timestamp = datetime.fromisoformat(data_str)
            msg = Mensagem(usuario, mensagem, id_msg, timestamp)
            mensagens_formatadas.append(msg.formatar()) # retorna as strings formatadas
        return jsonify(mensagens_formatadas), 200

    except (ChatError, DatabaseError) as e:
        log.error("[Erro] Falha ao listar as mensagens do banco de dados: %s", e)
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        log.error("[Erro] Fatal no endpoint de busca: %s", e)
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    log.info("Iniciando o servidor...")
    app.run(debug=True, port=5000)
