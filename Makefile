.PHONY: help install install-dev test lint format clean docker-up docker-down

help:
	@echo "Comandos disponibles:"
	@echo "  make install       - Instalar dependencias de producción"
	@echo "  make install-dev   - Instalar dependencias de desarrollo"
	@echo "  make test          - Ejecutar tests"
	@echo "  make lint          - Ejecutar linters"
	@echo "  make format        - Formatear código"
	@echo "  make clean         - Limpiar archivos temporales"
	@echo "  make docker-up     - Levantar servicios Docker"
	@echo "  make docker-down   - Detener servicios Docker"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/
	pylint src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.so" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov/

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down
