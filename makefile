# Define the environment and directories
VENV_DIR = .venv
DJANGO_DIR = EventsMarketPlace
FASTAPI_DIR = polling_service

# Define the commands
PYTHON = $(VENV_DIR)\Scripts\python
PIP = $(VENV_DIR)\Scripts\pip

# Setup virtual environment
.PHONY: venv
venv:
	python -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

# Install dependencies
.PHONY: install
install: venv
	$(PIP) install --user -r requirements.txt 

# Run Django server
.PHONY: run-django
run-django:
	cd $(DJANGO_DIR) && $(PYTHON) manage.py runserver

# Run FastAPI server
.PHONY: run-fastapi
run-fastapi:
	cd $(FASTAPI_DIR) && $(PYTHON) main.py

# Run both servers concurrently
.PHONY: run
run:
	start cmd /c "make run-django"
	start cmd /c "make run-fastapi"


# Clean up __pycache__ files
.PHONY: clean
clean:
	for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"


# Show help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  venv              - Create a virtual environment"
	@echo "  install           - Install dependencies"
	@echo "  run-django        - Run Django server"
	@echo "  run-fastapi       - Run FastAPI server"
	@echo "  run               - Run both Django and FastAPI servers"
	@echo "  clean             - Clean up __pycache__ files"
	@echo "  help              - Show this help message"
