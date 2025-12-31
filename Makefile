.PHONY: help test lint run dev docker-build docker-up docker-down clean deploy-local deploy-render

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

HELP_FUN = \
    %help%; \
    while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z0-9\-_]+)\s*:.*\#\#\#?(.*)?$$/ }; \
    print "usage: make [target]\n\n"; \
    for (sort keys %help) { \
        print "${WHITE}$$_:${RESET}\n"; \
        for (@{$$help{$$_}}) { \
            $$sep = " " x (44 - length $$_->[0]); \
            print "  ${CYAN}$$_->[0]$$sep${YELLOW}$$_->[1]${RESET}\n"; \
        }; \
        print "\n"; \
    }

help: ## Show this help
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

# ===== DEVELOPMENT =====
test: ## Run pytest with coverage
	pytest app/tests/ -v --cov=app --cov-report=html --cov-report=term-missing

test-fast: ## Run fast tests only
	pytest app/tests/ -v --maxfail=1 -m "not slow"

lint: ## Lint code with black/isort/mypy
	black app/ --check --diff
	isort app/ --check-only --diff
	mypy app/

lint-fix: ## Auto-fix linting issues
	black app/
	isort app/

run: ## Run development server
	uvicorn app.main:app --reload --port 8000

dev: ## Run with debug logging
	uvicorn app.main:app --reload --port 8000 --log-level debug

# ===== DOCKER =====
docker-build: ## Build Docker image
	docker build -t kasparro-backend:latest .

docker-up: ## Start docker-compose (build if needed)
	docker-compose up --build -d

docker-logs: ## View app logs
	docker-compose logs -f app

docker-down: ## Stop docker-compose
	docker-compose down

docker-db: ## Connect to postgres
	docker-compose exec postgres psql -U postgres -d kasparro

# ===== DEPLOYMENT =====
deploy-local: docker-down docker-up ## Local deployment

deploy-render: ## Deploy to Render (manual steps)
	@echo "$(GREEN)=== Render Deployment ===$(RESET)"
	@echo "$(YELLOW)1. Push to GitHub$(RESET)"
	@echo "$(YELLOW)2. Connect Render.com to repo$(RESET)"
	@echo "$(YELLOW)3. Build Command: make docker-build$(RESET)"
	@echo "$(YELLOW)4. Start Command: make run$(RESET)"
	@echo "$(CYAN)DOCKERFILE: ✅ Multi-stage optimized$(RESET)"
	@echo "$(CYAN)PORT: 8000$(RESET)"

# ===== CLEANUP =====
clean: ## Clean all artifacts
	rm -rf __pycache__ .pytest_cache htmlcov/ .coverage app.db logs/ .mypy_cache
	docker-compose down -v --remove-orphans 2>/dev/null || true
	docker system prune -f

clean-all: clean ## Clean everything including Docker images
	docker rmi kasparro-backend:latest 2>/dev/null || true
	docker volume prune -f

# ===== DATABASE =====
db-migrate: ## Run alembic migrations
	alembic upgrade head

db-init: ## Initialize alembic
	alembic init alembic

db-seed: ## Seed test data
	python -c "from app.scripts.seed_data import seed; import asyncio; asyncio.run(seed())"

# ===== INFO =====
info: ## Show project info
	@echo "$(GREEN)Kasparro Backend$(RESET)"
	@echo "$(CYAN)Version:$$(grep __version__ app/__init__.py | cut -d'\"' -f4)$(RESET)"
	@echo "$(CYAN)Python:$$(python --version)$(RESET)"
	@echo "$(CYAN)FastAPI Docs: http://localhost:8000/docs$(RESET)"
	@echo "$(CYAN)Health: http://localhost:8000/health/$(RESET)"
