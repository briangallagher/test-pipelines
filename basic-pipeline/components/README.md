# Components

## generate_data

- Purpose: Generate a small dataset (Hugging Face `datasets`) with fields `id`, `text`, `length`.
- Base image: `registry.access.redhat.com/ubi9/python-311:latest`
- Packages to install: `datasets`

Inputs (parameters):
- num_rows (int, default: 5)
- prefix (str, default: "item")

Outputs (artifacts):
- generated_dataset (system.Dataset): Directory written via `dataset.save_to_disk(path)`

Logging:
- Prints start/end messages and where the dataset is written.

Usage (pipeline):
- `gen_op = generate_data(...)
  gen_op.outputs["generated_dataset"] -> pass to downstream components`

---

## process_data

- Purpose: Load the dataset from step 1, filter by `min_length`, log metrics, and write a summary JSON.
- Base image: `registry.access.redhat.com/ubi9/python-311:latest`
- Packages to install: `datasets`

Inputs (artifacts/parameters):
- input_dataset (system.Dataset): Read via `load_from_disk(path)`
- min_length (int, default: 0)

Outputs (artifacts):
- output_metrics (system.Metrics): Logs `rows_total`, `rows_kept`
- output_results (system.Artifact): JSON summary written to `output_results.path`

Logging:
- Prints start/end messages, where it reads the dataset from, and where it writes the results.

---

## Building component YAMLs

Compile component specs to YAML files:

```bash
make build-components
```

This produces `components/generate_data_component.yaml` and `components/process_data_component.yaml`.
