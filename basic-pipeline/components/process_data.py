from kfp import dsl


@dsl.component(
    base_image="registry.access.redhat.com/ubi9/python-311:latest",
    packages_to_install=["datasets"],
)
def process_data(
    input_dataset: dsl.Input[dsl.Dataset],
    output_metrics: dsl.Output[dsl.Metrics],
    output_results: dsl.Output[dsl.Artifact],
    min_length: int = 0,
):
    """Process the dataset produced by generate_data and log simple metrics.

    Args:
        input_dataset (dsl.Input[dsl.Dataset]): Input dataset directory from step 1.
        output_metrics (dsl.Output[dsl.Metrics]): Metrics to log.
        output_results (dsl.Output[dsl.Artifact]): JSON results file.
        min_length (int): Minimum length filter applied to the text field.
    """
    import json
    from datasets import load_from_disk

    print("[process_data] Starting component")
    print(
        f"[process_data] Parameters -> min_length={min_length}; reading dataset from {input_dataset.path}"
    )
    dataset = load_from_disk(input_dataset.path)

    # Simple filtering and statistics
    filtered = dataset.filter(lambda ex: int(ex.get("length", 0)) >= int(min_length))
    count_all = len(dataset)
    count_filtered = len(filtered)

    # Log metrics (avoid zero values if target UI ignores them)
    if count_all:
        output_metrics.log_metric("rows_total", float(count_all))
    if count_filtered:
        output_metrics.log_metric("rows_kept", float(count_filtered))
    # Dummy/derived metrics to ensure visibility at end of run
    output_metrics.log_metric("dummy_score", 1.0)
    if count_all:
        keep_ratio_percent = (count_filtered / count_all) * 100.0
        if keep_ratio_percent:
            output_metrics.log_metric("keep_ratio_percent", float(keep_ratio_percent))

    # Persist a small summary JSON
    summary = {
        "rows_total": count_all,
        "rows_kept": count_filtered,
        "min_length": int(min_length),
        "example_first": filtered[0] if count_filtered > 0 else None,
    }

    output_results.name = "results.json"
    print(f"[process_data] Writing results summary to {output_results.path}")
    with open(output_results.path, "w") as f:
        json.dump(summary, f, indent=2)
    print("[process_data] Finished component")


if __name__ == "__main__":
    import kfp

    kfp.compiler.Compiler().compile(
        process_data,
        package_path=__file__.replace(".py", "_component.yaml"),
    )


