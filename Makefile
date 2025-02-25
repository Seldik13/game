.PHONY: lint
lint:
	@echo "Linting start"
	pylint .\internal
	@echo "Linting completed"

.PHONY: install
install:
	@echo "Installing dependencies"
	.venv/Scripts/pip install -r ./.requirements