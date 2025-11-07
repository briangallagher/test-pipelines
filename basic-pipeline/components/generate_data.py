from kfp import dsl


@dsl.component(
    base_image="registry.access.redhat.com/ubi9/python-311:latest",
    packages_to_install=["datasets"],
)
def generate_data(
    generated_dataset: dsl.Output[dsl.Dataset],
    num_rows: int = 5,
    prefix: str = "item",
):
    """Generate a tiny dataset and save it as a Hugging Face Dataset.

    Args:
        generated_dataset (dsl.Output[dsl.Dataset]): Output dataset directory.
        num_rows (int): Number of rows to generate.
        prefix (str): Text prefix used for the generated content.
    """
    from datasets import Dataset

    print("[generate_data] Starting component")
    print(
        f"[generate_data] Parameters -> num_rows={num_rows}, prefix='{prefix}'"
    )

    rows = []
    for i in range(num_rows):
        rows.append({"id": i, "text": f"{prefix}-{i}", "length": len(f"{prefix}-{i}")})

    dataset = Dataset.from_list(rows)

    # Persist to output artifact path
    print(
        f"[generate_data] Writing dataset with {len(rows)} rows to {generated_dataset.path}"
    )
    dataset.save_to_disk(generated_dataset.path)
    print("[generate_data] Finished component")


if __name__ == "__main__":
    import kfp

    kfp.compiler.Compiler().compile(
        generate_data,
        package_path=__file__.replace(".py", "_component.yaml"),
    )


