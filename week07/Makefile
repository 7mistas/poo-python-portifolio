.PHONY: help build up down restart logs shell test clean

help:
	@echo "Chat AWS - Comandos Docker"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  make build     - Construir imagem Docker"
	@echo "  make up        - Subir containers"
	@echo "  make down      - Parar containers"
	@echo "  make restart   - Reiniciar containers"
	@echo ""
	@echo "Monitoramento:"
	@echo "  make logs      - Ver logs em tempo real"
	@echo "  make status    - Status dos containers"
	@echo "  make shell     - Acessar shell do container"
	@echo ""
	@echo "Desenvolvimento:"
	@echo "  make test      - Rodar testes"
	@echo "  make clean     - Limpar containers e volumes"
	@echo ""

build:
	@echo "Construindo imagem Docker..."
	docker compose build
up:
	@echo "Subindo containers..."
	docker compose up -d
	@echo "API do ChatAWS disponível em http://localhost:5000"
	@echo "Documentação em http://localhost:5000/docs"
down:
	@echo "Parando containers..."
	docker compose down
restart:
	@echo "Reiniciando containers..."
	docker compose restart
logs:
	@echo "Logs dos containers (Ctrl+C para sair):"
	docker compose logs -f
status:
	@echo "Status dos containers:"
	dockercompose ps
shell:
	@echo "Acessando shell do container..."
	docker compose exec api /bin/bash
test:
	@echo "Rodando testes..."
	docker compose exec api pytest -v
clean:
	@echo "Limpando containers e volumes..."
	docker compose down -v
	@echo "Limpeza concluída"
rebuild: clean build up
	@echo "Rebuild completo concluído"
