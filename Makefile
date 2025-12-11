.PHONY: dev dev-build prod clean nuke

# Desenvolvimento com hot reload (sem rebuild a cada mudança de código)
dev:
	docker compose -f docker-compose.dev.yml up

# Desenvolvimento com rebuild (usar quando mudar dependências)
dev-build:
	docker compose -f docker-compose.dev.yml up --build

# Produção com build completo (sem carregar dados seed)
prod:
	docker compose up --build

# Para os containers e remove volumes do compose
clean:
	docker compose down -v
	docker compose -f docker-compose.dev.yml down -v

# Limpeza total: remove containers, imagens, volumes e cache
nuke:
	docker compose down -v
	docker compose -f docker-compose.dev.yml down -v
	docker system prune -a --volumes -f
	docker volume prune -a -f
