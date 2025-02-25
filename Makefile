.PHONY: lint
lint:
	@echo "Linting start"
	.venv/Scripts/pylint --rcfile=./.pylintrc .\internal
	@echo "Linting completed"

.PHONY: install
install:
	@echo "Installing dependencies"
	.venv/Scripts/pip install -r ./.requirements