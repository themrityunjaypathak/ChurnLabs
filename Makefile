# Shell
# ------------------------------------------------
SHELL := /bin/bash

# Project Variables
# ------------------------------------------------
API_NAME        = churn_api
API_PORT        = 8000
FRONTEND_NAME   = churn_frontend
FRONTEND_PORT   = 3000
APP             = api.main:app
UV              = uv
UV_RUN          = uv run
PYTHON          = uv run python


# Dependency Management
# ------------------------------------------------
install:
	$(UV) sync

install-dev:
	$(UV) sync --extra dev

lock:
	$(UV) lock


# Experimentation
# ------------------------------------------------
mlflow-ui:
	$(UV_RUN) mlflow ui

mlflow-clean:
	rm -rf mlartifacts mlflow.db


# API
# ------------------------------------------------
api-dev:
	$(UV_RUN) uvicorn $(APP) --reload

api-prod:
	$(UV_RUN) uvicorn $(APP) --host 0.0.0.0 --port $(API_PORT)


# Frontend
# ------------------------------------------------
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

frontend-serve:
	cd frontend && npm run preview


# End-to-End ML Pipeline
# ------------------------------------------------
ingest:
	$(PYTHON) scripts/run_ingestion.py

preprocess: ingest
	$(PYTHON) scripts/run_preprocessing.py

train: preprocess
	$(PYTHON) scripts/run_training.py

pipeline: train


# Docker (API)
# ------------------------------------------------
docker-api-build:
	docker build -f api/Dockerfile -t $(API_NAME) .

docker-api-run:
	docker rm -f $(API_NAME) || true
	docker run -d \
		-p $(API_PORT):8000 \
		--env-file .env \
		--name $(API_NAME) \
		$(API_NAME)

docker-api-stop:
	docker stop $(API_NAME) || true

docker-api-clean:
	docker rm -f $(API_NAME) || true
	docker rmi $(API_NAME) || true


# Docker (Frontend)
# ------------------------------------------------
docker-frontend-build:
	docker build \
		--build-arg VITE_API_URL=http://localhost:$(API_PORT) \
		-t $(FRONTEND_NAME) \
		./frontend

docker-frontend-run:
	docker rm -f $(FRONTEND_NAME) || true
	docker run -d \
		-p $(FRONTEND_PORT):80 \
		--name $(FRONTEND_NAME) \
		$(FRONTEND_NAME)

docker-frontend-stop:
	docker stop $(FRONTEND_NAME) || true

docker-frontend-clean:
	docker rm -f $(FRONTEND_NAME) || true
	docker rmi $(FRONTEND_NAME) || true


# Docker Compose
# ------------------------------------------------
docker-login:
	docker login

compose-build:
	docker compose build

compose-up:
	docker compose up -d

compose-up-build:
	docker compose up --build -d

compose-push:
	docker compose push

compose-down:
	docker compose down

compose-clean:
	docker compose down -v
	docker system prune -f


# Utilities
# ------------------------------------------------
reset-venv:
	rm -rf .venv uv.lock


# Help
# ------------------------------------------------
help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "Dependency Management:"
	@echo "  make install                   - Install project dependencies"
	@echo "  make install-dev               - Install dependencies with dev extras"
	@echo "  make lock                      - Update dependency lock file"
	@echo ""
	@echo "Experimentation:"
	@echo "  make mlflow-ui                 - Launch MLflow tracking UI"
	@echo "  make mlflow-clean              - Delete MLflow artifacts and database"
	@echo ""
	@echo "API:"
	@echo "  make api-dev                   - Run FastAPI with auto-reload (development)"
	@echo "  make api-prod                  - Run FastAPI server (production)"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-install          - Install frontend dependencies"
	@echo "  make frontend-dev              - Start frontend dev server"
	@echo "  make frontend-build            - Build frontend for production"
	@echo "  make frontend-serve            - Preview production build locally"
	@echo ""
	@echo "End-to-End ML Pipeline:"
	@echo "  make ingest                    - Run data ingestion pipeline"
	@echo "  make preprocess                - Run preprocessing pipeline"
	@echo "  make train                     - Run training pipeline"
	@echo "  make pipeline                  - Run full pipeline (ingest → preprocess → train)"
	@echo ""
	@echo "Docker (API):"
	@echo "  make docker-api-build          - Build API Docker image"
	@echo "  make docker-api-run            - Run API container"
	@echo "  make docker-api-stop           - Stop API container"
	@echo "  make docker-api-clean          - Remove API container and image"
	@echo ""
	@echo "Docker (Frontend):"
	@echo "  make docker-frontend-build     - Build frontend Docker image"
	@echo "  make docker-frontend-run       - Run frontend container"
	@echo "  make docker-frontend-stop      - Stop frontend container"
	@echo "  make docker-frontend-clean     - Remove frontend container and image"
	@echo ""
	@echo "Docker Compose:"
	@echo "  make docker-login              - Login to Docker Hub"
	@echo "  make compose-build             - Build all services"
	@echo "  make compose-up                - Start all services"
	@echo "  make compose-up-build          - Build and start all services"
	@echo "  make compose-push              - Push all images to Docker Hub"
	@echo "  make compose-down              - Stop all services"
	@echo "  make compose-clean             - Remove containers, volumes, and unused data"
	@echo ""
	@echo "Utilities:"
	@echo "  make reset-venv                - Remove virtual environment"
	@echo ""