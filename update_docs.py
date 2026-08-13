import os
import re

def main():
    dir_path = "docs/datasets"
    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} not found.")
        return
        
    for filename in os.listdir(dir_path):
        if not filename.endswith(".md"): 
            continue
        path = os.path.join(dir_path, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace CLI
        content = re.sub(
            r'python download_dataset\.py --name ([\w-]+) --source (\w+) --output-dir [^\s]+ --format (parquet|csv)',
            r'python download_dataset.py --names \1 --source \2 --output-dir ./data --format \3',
            content
        )
        
        # Replace Python API
        content = re.sub(
            r'dataset, var_types, target_col, prediction_task, metadata = mixtabank\.dataset_loader\(\s*name="([\w-]+)", source="(\w+)", df_type="polars"\s*\)',
            r'# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)\n# (Also uses curated=True to apply any JSON recipes automatically)\ndataset = mixtabank.dataset_loader(\n    name="\1", source="\2", curated=True\n)\n\n# Access the raw Polars DataFrame\ndf = dataset.data',
            content
        )
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("Successfully updated all dataset markdown documentation files!")

if __name__ == "__main__":
    main()
