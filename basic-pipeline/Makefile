PYTHON := python
KFP_SRC ?= ../pipelines

.PHONY: build
build:
	uv run $(PYTHON) basic_two_step_pipeline.py

.PHONY: kfp-dev
# Install KFP from a local kubeflow/pipelines repo in editable mode.
# Usage: make kfp-dev KFP_SRC=/absolute/path/to/pipelines
kfp-dev:
	@if [ -z "$(KFP_SRC)" ]; then \
		echo "Error: KFP_SRC is not set. Example: make kfp-dev KFP_SRC=/path/to/pipelines"; \
		exit 1; \
	fi
	# Ensure we're on Python 3.11 per project constraint
	uv python install 3.11
	uv python pin 3.11
	uv sync
	# Generate Python artifacts (protos) in the KFP repo
	uv run $(PYTHON) "$(KFP_SRC)/api/v2alpha1/python/generate_proto.py"
	# Install editable packages into this project's venv
	uv pip install -e "$(KFP_SRC)/api/v2alpha1/python" --config-settings editable_mode=strict
	uv pip install -e "$(KFP_SRC)/sdk/python" --config-settings editable_mode=strict
	uv pip install -e "$(KFP_SRC)/kubernetes_platform/python" --config-settings editable_mode=strict
	@echo "Installed KFP (sdk/api/kubernetes_platform) from local repo: $(KFP_SRC)"

.PHONY: build-dev
build-dev: kfp-dev
	uv run $(PYTHON) basic_two_step_pipeline.py

.PHONY: build-components
build-components:
	uv run $(PYTHON) components/generate_data.py
	uv run $(PYTHON) components/process_data.py


