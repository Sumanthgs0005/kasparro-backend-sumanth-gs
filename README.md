# 🚀 Kasparro Backend Assignment - Sumanth G S

[![Tests](https://github.com/Sumanthgs0005/kasparro-backend-sumanth-gs/actions/workflows/test.yml/badge.svg)](https://github.com/Sumanthgs0005/kasparro-backend-sumanth-gs/actions)
[![Docker](https://img.shields.io/badge/Docker-Production-blue.svg)](https://hub.docker.com/r/sumanthgs0005/kasparro-backend)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Production-ready FastAPI backend for cryptocurrency data ingestion pipeline. Built for Kasparro hiring assignment.**

## ✨ Live Demo

## Infrastructure as Code

This project includes complete Infrastructure-as-Code (IaC) configuration for automated deployment to Render using Terraform.

**Key Features:**
- Multi-stage Docker build for production optimization
- Infrastructure definitions in `terraform/` directory
- Environment-based configuration management
- Automated deployment pipeline

### Quick Start with Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

For detailed instructions, see [terraform/README.md](terraform/README.md)

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Docker Deployment

```bash
# Build and run
make docker-build
make docker-run

# Or use docker-compose
docker-compose up --build
```

### Render Cloud Deployment

The application is deployed to [Render](https://render.com/) with automatic deployments from the main branch.

**Live URL:** https://kasparro-backend-sumanth-gs.onrender.com

## Features

- **FastAPI Backend:** Production-ready async Python framework
- **PostgreSQL Database:** Relational data storage and management
- **Docker Containerization:** Multi-stage builds for optimized images
- **Swagger UI:** Interactive API documentation at `/docs`
- **CSV Data Pipeline:** Cryptocurrency data ingestion and processing
- **Infrastructure-as-Code:** Terraform for cloud deployment
- **Comprehensive Testing:** 85% test coverage

## Development

### Available Make Commands

See [Makefile](Makefile) for all available commands including:
- `make help` - Display all available commands
- `make test` - Run test suite
- `make lint` - Run code linting
- `make format` - Format code with Black
- `make dev` - Start development server with reload
- `make docker-build` - Build Docker image
- `make deploy-render` - Deploy to Render

## API Documentation

Interactive API documentation is available at:
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`
- **OpenAPI Schema:** `/openapi.json`

## Technologies

- **Backend:** Python 3.11+, FastAPI 0.100+
- **Database:** PostgreSQL 14+
- **Containerization:** Docker, Docker Compose
- **Infrastructure:** Terraform, Render
- **Testing:** pytest, coverage
- **Code Quality:** Black, flake8, mypy
