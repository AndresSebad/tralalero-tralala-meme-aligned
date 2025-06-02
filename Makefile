VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip
SPACE_DIR=src/app
SPACE_ID?=somosnlp-hackathon-2025/tralalelo-tralala-demo
SPACE_TYPE=gradio

push_app_hf:
	@echo "🚀 Subiendo app desde $(SPACE_DIR) a Hugging Face Space $(SPACE_ID)..."
	@$(PYTHON) -m pip install -q huggingface_hub  # Asegura que huggingface_hub esté disponible
	@python -c "from huggingface_hub import create_repo, upload_folder; \
create_repo('$(SPACE_ID)', repo_type='space', space_sdk='$(SPACE_TYPE)', exist_ok=True); \
upload_folder(folder_path='$(SPACE_DIR)', repo_id='$(SPACE_ID)', repo_type='space')"
	@echo "✅ App subida con éxito a https://huggingface.co/spaces/$(SPACE_ID)"

init:
	@echo "🔧 Creando entorno virtual en $(VENV_DIR)..."
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@echo "✅ Entorno virtual listo."

	@if [ -f requirements.txt ]; then \
		echo "📦 Instalando dependencias desde requirements.txt..."; \
		$(PIP) install --upgrade pip && $(PIP) install -r requirements.txt; \
	else \
		echo "⚠️  No se encontró requirements.txt, omitiendo instalación de dependencias."; \
	fi
	@echo "✅ Todo listo. Activa el entorno con: source .venv/bin/activate"

activate:
	@echo "⚠️  No se puede activar el entorno desde Makefile."
	@echo "👉 Usa: source .venv/bin/activate"