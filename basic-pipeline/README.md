# Basic Two-Step KFP Pipeline

This folder contains a minimal Kubeflow Pipelines (KFP) v2 example that mirrors the
I/O patterns used in the IBM TechXchange sample, but with two simple steps:

- generate_data: produces a small Hugging Face Dataset artifact
- process_data: consumes that Dataset, logs metrics, and writes a JSON summary

The project is managed via `uv`. By default it uses a stable KFP release, but you can switch
to a local master checkout of KFP with editable installs (see below).

---

## Prerequisites

- Python 3.11
- `uv` installed (`pipx install uv` or see uv docs)
- brew install protobuf (on mac)
---

## Install dependencies

Sync the environment (creates/updates a local `.venv`):

```bash
uv sync
```

---

## Build (compile pipeline to YAML)

Compile the pipeline to `basic_two_step_pipeline.yaml`:

```bash
make build
```

Or run directly without Make:

```bash
uv run python basic_two_step_pipeline.py
```

To compile component YAMLs (for reuse elsewhere):

```bash
make build-components
```

---

## Components

- `components/generate_data.py`
  - Inputs: `num_rows: int`, `prefix: str`
  - Outputs: `generated_dataset: system.Dataset`
  - Creates a small dataset with fields: `id`, `text`, `length`
  - Logs start/end and where it writes the dataset

- `components/process_data.py`
  - Inputs: `input_dataset: system.Dataset`, `min_length: int`
  - Outputs: `output_metrics: system.Metrics`, `output_results: system.Artifact`
  - Loads the dataset, filters by `length >= min_length`, logs row counts, and
    writes a `results.json`
  - Logs start/end, where it reads the dataset from, and where it writes results

Both components include a `__main__` block to compile each component to YAML if
run directly, similar to the IBM example.

---

## Pipeline

- `basic_two_step_pipeline.py`
  - Parameters: `num_rows`, `prefix`, `min_length`
  - Step 1: `generate_data` produces a Dataset
  - Step 2: `process_data` consumes the Dataset and produces metrics + results
  - Includes a compile block that writes `basic_two_step_pipeline.yaml`

---

## Notes

- Component containers install runtime libs via `packages_to_install` so they do
  not need to be added to the project dependencies.

---

## Using KFP master from a local checkout (editable)

If you have the `kubeflow/pipelines` repo locally and want to use its master branch:

```bash
# Example path to your KFP repo
export KFP_SRC=/absolute/path/to/pipelines

# Install the local KFP packages into this project's venv (editable)
make kfp-dev KFP_SRC=$KFP_SRC

# Build the pipeline using the local KFP
make build
```

What the target does:
- Ensures Python 3.11 is active for this project
- Runs `make -C $KFP_SRC/api python-dev` to generate Python artifacts
- Installs editable packages:
  - `$KFP_SRC/api/v2alpha1/python` (kfp-pipeline-spec)
  - `$KFP_SRC/sdk/python` (kfp)
  - `$KFP_SRC/kubernetes_platform/python` (kfp-kubernetes)

To revert to the stable KFP dependency from `pyproject.toml`, re-run:

```bash
uv sync
```


