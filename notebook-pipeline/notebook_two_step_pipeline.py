import os
import shutil

import kfp
from kfp import dsl


@dsl.notebook_component(
    notebook_path=os.path.join("notebooks", "generate_data.ipynb"),
    packages_to_install=["datasets", "nbclient", "nbformat", "ipykernel"],
)
def nb_generate_data(
    generated_dataset: dsl.Output[dsl.Dataset],
    num_rows: int = 5,
    prefix: str = "item",
    seed: int = 42,
):
    import shutil
    print("[nb_generate_data] Starting component")
    print(
        f"[nb_generate_data] Params -> num_rows={num_rows}, prefix={prefix}, seed={seed}"
    )
    dsl.run_notebook(num_rows=num_rows, prefix=prefix, seed=seed)

    # Notebook writes to /tmp/kfp_nb_outputs/dataset
    src_dir = "/tmp/kfp_nb_outputs/dataset"
    print(
        f"[nb_generate_data] Copying notebook output from {src_dir} to {generated_dataset.path}"
    )
    shutil.copytree(src_dir, generated_dataset.path, dirs_exist_ok=True)
    print("[nb_generate_data] Finished component")


@dsl.notebook_component(
    notebook_path=os.path.join("notebooks", "process_data.ipynb"),
    packages_to_install=["datasets", "nbclient", "nbformat", "ipykernel"],
)
def nb_process_data(
    input_dataset: dsl.Input[dsl.Dataset],
    output_metrics: dsl.Output[dsl.Metrics],
    output_results: dsl.Output[dsl.Artifact],
    min_length: int = 0,
):
    import shutil
    print("[nb_process_data] Starting component")
    print(
        f"[nb_process_data] Params -> min_length={min_length}; reading dataset from {input_dataset.path}"
    )

    dsl.run_notebook(
        input_dataset_path=input_dataset.path,
        min_length=min_length,
    )

    # Results and metrics are written by the notebook under /tmp/kfp_nb_outputs
    results_path = "/tmp/kfp_nb_outputs/results.json"
    metrics_path = "/tmp/kfp_nb_outputs/metrics.json"

    print(f"[nb_process_data] Reading metrics from {metrics_path}")
    import json
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics_dict = json.load(f)

    # Log metrics (avoid zero if your UI ignores zeros)
    for key, value in metrics_dict.items():
        if isinstance(value, (int, float)) and value != 0:
            output_metrics.log_metric(key, float(value))

    print(f"[nb_process_data] Copying results to {output_results.path}")
    output_results.name = "results.json"
    shutil.copy(results_path, output_results.path)

    print("[nb_process_data] Finished component")


@dsl.pipeline(
    name="Notebook two-step pipeline",
    description="Use notebook components to generate and process a dataset.",
)
def notebook_two_step_pipeline(
    num_rows: int = 5,
    prefix: str = "item",
    min_length: int = 0,
    seed: int = 42,
):
    # Step 1: Generate dataset via notebook component
    gen_op = (
        nb_generate_data(num_rows=num_rows, prefix=prefix, seed=seed)
        .set_caching_options(enable_caching=False)
    )

    # Step 2: Process dataset via notebook component
    _ = (
        nb_process_data(
            input_dataset=gen_op.outputs["generated_dataset"],
            min_length=min_length,
        )
        .after(gen_op)
        .set_caching_options(enable_caching=False)
    )


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        pipeline_func=notebook_two_step_pipeline,
        package_path=__file__.replace(".py", ".yaml"),
    )


