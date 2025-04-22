# Variables
PYTHON = python
MANAGE = $(PYTHON) manage.py
CRAWLER_DIR = core/apps/crawler
PRICING_DIR = core/apps/pricing_dular1

# Mark all targets as phony since they don't produce files
.PHONY: help \
        madeira mercado_livre magalu carrefas leroy \
        build docker attach \
        shell runserver migrate makemigrations test collectstatic clean

# Default target - shows help
help:
	@echo "Available commands:"
	@echo ""
	@echo "CRAWLER COMMANDS:"
	@echo "  make madeira         - Run madeira spider"
	@echo "  make mercado_livre   - Run MercadoLivre crawler"
	@echo "  make magalu          - Run Magalu crawler"
	@echo "  make carrefas        - Run Carrefas crawler"
	@echo "  make leroy           - Run Leroy crawler"
	@echo ""
	@echo "DOCKER COMMANDS:"
	@echo "  make build           - Build Docker image"
	@echo "  make docker          - Run development container"
	@echo "  make attach          - Attach to running container"
	@echo ""
	@echo "DJANGO COMMANDS:"
	@echo "  make shell           - Run Django interactive shell"
	@echo "  make runserver       - Start Django development server"
	@echo "  make migrate         - Apply database migrations"
	@echo "  make makemigrations  - Create new migrations based on model changes"
	@echo "  make test            - Run Django tests"
	@echo "  make collectstatic   - Collect static files"
	@echo ""
	@echo "MAINTENANCE COMMANDS:"
	@echo "  make clean           - Remove Python bytecode files and other artifacts"

# Crawler commands
madeira:
	cd $(PRICING_DIR) && $(PYTHON) spider_madeira_async.py

mercado_livre:
	cd $(CRAWLER_DIR) && scrapy crawl ml_simple_db

magalu:
	cd $(CRAWLER_DIR) && scrapy crawl magalu_simple_db

carrefas:
	cd $(CRAWLER_DIR) && scrapy crawl carrefas_simple_db

leroy:
	cd $(CRAWLER_DIR) && scrapy crawl leroy_simple_db

# Docker commands
build:
	docker build . -t scrapy

docker:
	docker compose run --rm dev

attach:
	docker exec -it scrapy /bin/bash

# Django management commands
shell:
	$(MANAGE) shell

runserver:
	$(MANAGE) runserver

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

test:
	$(MANAGE) test

collectstatic:
	$(MANAGE) collectstatic --noinput

# Maintenance commands
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name "*.pyo" -delete
	find . -name "*.~" -delete