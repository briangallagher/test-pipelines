PYTHON := python

# KFP_SRC points to your local kubeflow/pipelines clone used for dev installs.
# Defaults to ../pipelines (a sibling of this folder). Override like:
#   make build-dev KFP_SRC=/absolute/path/to/pipelines
KFP_SRC ?= ../pipelines

.PHONY: build
# Compile the notebook pipeline to YAML using the project's pinned dependencies.
# Output: notebook_two_step_pipeline.yaml in this directory.
build:
	uv run $(PYTHON) notebook_two_step_pipeline.py

.PHONY: kfp-dev
# Prepare a dev environment using your local KFP repo (editable installs).
# This ensures SDK/proto versions match master in your clone.
kfp-dev:
	uv python install 3.11
	uv python pin 3.11
	uv sync
	uv run $(PYTHON) "$(KFP_SRC)/api/v2alpha1/python/generate_proto.py"
	uv pip install -e "$(KFP_SRC)/api/v2alpha1/python" --config-settings editable_mode=strict
	uv pip install -e "$(KFP_SRC)/sdk/python" --config-settings editable_mode=strict
	uv pip install -e "$(KFP_SRC)/kubernetes_platform/python" --config-settings editable_mode=strict

.PHONY: build-dev
# Compile the notebook pipeline to YAML after setting up local KFP (editable).
# Useful when testing against KFP master without changing pyproject deps.
build-dev: kfp-dev
	uv run $(PYTHON) notebook_two_step_pipeline.py


