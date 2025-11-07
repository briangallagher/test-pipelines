# Notebook Two-Step KFP Pipeline

Notebook-based version of the basic two-step pipeline. Each step is a notebook wrapped by `@dsl.notebook_component`.

- notebooks/generate_data.ipynb: creates a small dataset and saves it under `/tmp/kfp_nb_outputs/dataset`
- notebooks/process_data.ipynb: reads the dataset, computes metrics and summary, writes
  `/tmp/kfp_nb_outputs/metrics.json` and `/tmp/kfp_nb_outputs/results.json`

The Python wrappers copy notebook outputs into KFP artifacts and log metrics.

---

## Build (compile to YAML)

```bash
make build
# emits notebook_two_step_pipeline.yaml
```

To use local KFP master (editable installs), run:

```bash
make build-dev
```

---

## I/O contracts

- nb_generate_data
  - Inputs: `num_rows: int`, `prefix: str`
  - Outputs: `generated_dataset: system.Dataset` (copied from `/tmp/kfp_nb_outputs/dataset`)

- nb_process_data
  - Inputs: `input_dataset: system.Dataset`, `min_length: int`
  - Outputs:
    - `output_metrics: system.Metrics` (logs `rows_total`, `rows_kept`, `dummy_score`, `keep_ratio_percent` if > 0)
    - `output_results: system.Artifact` (JSON summary copied from `/tmp/kfp_nb_outputs/results.json`)

---

## Logging

Both notebooks and wrappers print start/end messages and where files are read/written.


