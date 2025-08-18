# PolishPad Makefile
# AI-powered text polisher tool

# Variables
PYTHON := python3
VENV_DIR := .venv
VENV_ACTIVATE := $(VENV_DIR)/bin/activate
PIP := $(VENV_DIR)/bin/pip
PYTHON_VENV := $(VENV_DIR)/bin/python
REQUIREMENTS := requirements.txt
SCRIPT := polish_clipboard.py

# Detect OS for different commands
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    # macOS
    ACTIVATE_CMD := source $(VENV_ACTIVATE)
else
    # Linux/Unix
    ACTIVATE_CMD := source $(VENV_ACTIVATE)
endif

# Default target
.PHONY: help
help:
	@echo "PolishPad - AI-powered text polisher"
	@echo ""
	@echo "Available targets:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  install   - Install/update dependencies"
	@echo "  run       - Run the polish clipboard tool (hotkey mode)"
	@echo "  test      - Test with sample text"
	@echo "  clean     - Remove virtual environment"
	@echo "  status    - Check setup status"
	@echo ""
	@echo "Environment variables (set before running):"
	@echo "  OPENAI_API_KEY   - Required for OpenAI provider"
	@echo "  POLISH_PROVIDER  - 'openai' (default) or 'ollama'"
	@echo "  POLISH_MODEL     - Model to use (gpt-4o-mini, llama3.1:8b, etc.)"
	@echo "  POLISH_TONE      - 'polite' (default), 'formal', 'friendly', 'concise'"

# Check if virtual environment exists
.PHONY: check-venv
check-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment not found. Creating..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi

# Create virtual environment and install dependencies
.PHONY: setup
setup: check-venv
	@echo "Setting up PolishPad..."
	@$(ACTIVATE_CMD) && $(PIP) install --upgrade pip
	@$(ACTIVATE_CMD) && $(PIP) install -r $(REQUIREMENTS)
	@echo "Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Set your API key: export OPENAI_API_KEY='your-key-here'"
	@echo "2. Run the tool: make run"

# Install/update dependencies
.PHONY: install
install: check-venv
	@echo "Installing dependencies..."
	@$(ACTIVATE_CMD) && $(PIP) install --upgrade pip
	@$(ACTIVATE_CMD) && $(PIP) install -r $(REQUIREMENTS)
	@echo "Dependencies installed!"

# Run the polish clipboard tool in hotkey mode
.PHONY: run
run: check-venv
	@echo "Starting PolishPad (hotkey mode)..."
	@echo "Press Ctrl+C to stop"
	@$(ACTIVATE_CMD) && $(PYTHON_VENV) $(SCRIPT)

# Test the tool with sample text
.PHONY: test
test: check-venv
	@echo "Testing PolishPad with sample text..."
	@$(ACTIVATE_CMD) && $(PYTHON_VENV) $(SCRIPT) "hey can u plz send me the report asap thx"

# Check current setup status
.PHONY: status
status:
	@echo "PolishPad Setup Status:"
	@echo "======================="
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "✓ Virtual environment: EXISTS"; \
	else \
		echo "✗ Virtual environment: MISSING"; \
	fi
	@if [ -f "$(REQUIREMENTS)" ]; then \
		echo "✓ Requirements file: EXISTS"; \
	else \
		echo "✗ Requirements file: MISSING"; \
	fi
	@if [ -f "$(SCRIPT)" ]; then \
		echo "✓ Main script: EXISTS"; \
	else \
		echo "✗ Main script: MISSING"; \
	fi
	@echo ""
	@echo "Environment variables:"
	@if [ -n "$$OPENAI_API_KEY" ]; then \
		echo "✓ OPENAI_API_KEY: SET"; \
	else \
		echo "✗ OPENAI_API_KEY: NOT SET"; \
	fi
	@echo "  POLISH_PROVIDER: $${POLISH_PROVIDER:-openai (default)}"
	@echo "  POLISH_MODEL: $${POLISH_MODEL:-gpt-4o-mini (default)}"
	@echo "  POLISH_TONE: $${POLISH_TONE:-polite (default)}"

# Clean up - remove virtual environment
.PHONY: clean
clean:
	@echo "Removing virtual environment..."
	@rm -rf $(VENV_DIR)
	@echo "Cleaned up!"

# Reinstall everything from scratch
.PHONY: reinstall
reinstall: clean setup

# Show package list
.PHONY: freeze
freeze: check-venv
	@$(ACTIVATE_CMD) && $(PIP) freeze

# Update requirements.txt with current packages
.PHONY: update-requirements
update-requirements: check-venv
	@$(ACTIVATE_CMD) && $(PIP) freeze > $(REQUIREMENTS)
	@echo "Updated $(REQUIREMENTS)"

# Development mode - install in editable mode
.PHONY: dev
dev: setup
	@echo "Development setup complete"

# Check for updates to packages
.PHONY: check-updates
check-updates: check-venv
	@$(ACTIVATE_CMD) && $(PIP) list --outdated
