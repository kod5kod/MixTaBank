import os
import json
import subprocess
import shutil

# Paths
WIKI_DIR = ".wiki_repo"
UCI_JSON = "mixtabank/data_src_dict/UCI.JSON"
KAGGLE_JSON = "mixtabank/data_src_dict/Kaggle.JSON"
WIKI_REPO_URL = "git@github.com:kod5kod/MixTaBank.wiki.git"

def run_cmd(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr}")
        raise RuntimeError(f"Command failed: {result.stderr}")
    print(result.stdout)

def extract_dataset_table_from_readme():
    table_lines = []
    in_table = False
    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            for line in f:
                if line.strip().startswith("| # | Dataset name"):
                    in_table = True
                if in_table:
                    if line.strip().startswith("|"):
                        table_lines.append(line)
                    else:
                        break
    return "".join(table_lines)

def generate_core_pages():
    dataset_table = extract_dataset_table_from_readme()
    
    home_content = f"""# MixTaBank
Welcome to the MixTaBank Wiki! MixTaBank is a collection of heterogeneous mixed-type tabular datasets tailored for evaluating tabular generative models under realistic, human-centric conditions.

## Quick Links
- [[Installation & Setup|Installation-&-Setup]]
- [[CLI Downloader Guide|CLI-Downloader-Guide]]
- [[Python API Reference|Python-API-Reference]]
- [[Contributing Guide|Contributing-Guide]]

## Dataset Guide
{dataset_table}
"""
    with open(os.path.join(WIKI_DIR, "Home.md"), "w") as f:
        f.write(home_content)

    install_content = """# Installation & Setup
To install MixTaBank, you can use Conda or Virtualenv.

```bash
git clone https://github.com/kod5kod/MixTaBank.git
cd MixTaBank

# Conda Env:
conda create -n mixtabank python=3.13
conda activate mixtabank
pip install -r requirements.txt
```
"""
    with open(os.path.join(WIKI_DIR, "Installation-&-Setup.md"), "w") as f:
        f.write(install_content)

    cli_content = """# CLI Downloader Guide
MixTaBank includes a convenient CLI script, `download_dataset.py`, to fetch datasets, perform splits, and save the data.

### Usage
```bash
python download_dataset.py --name bank-marketing --output-dir ./data/bank --format parquet
```
"""
    with open(os.path.join(WIKI_DIR, "CLI-Downloader-Guide.md"), "w") as f:
        f.write(cli_content)

    api_content = """# Python API Reference
You can import functions directly from the `mixtabank` module.
- `dataset_loader(name, source, df_type)`: Loads a dataset.
- `get_df_info_pl(df)`: Retrieves information for a Polars dataframe.
- `get_df_info_pd(df)`: Retrieves information for a Pandas dataframe.
- `pl_train_valid_test_split`: Splits Polars dataframe.
- `pd_train_valid_test_split`: Splits Pandas dataframe.
- `generate_dataset_info_json`: Generates standard metadata JSON.
"""
    with open(os.path.join(WIKI_DIR, "Python-API-Reference.md"), "w") as f:
        f.write(api_content)
        
    contrib_content = """# Contributing Guide & Citation
We welcome contributions! Please open issues or submit pull requests.

## How to Cite
If you use this library or benchmark in your work, please cite:
```bibtex
@article{mixtabank2025,
  title={Grounding Tabular Generative Models in Reality: A Benchmark for Human-Centered Evaluation},
  author={MixTaBank Authors},
  journal={Under Review},
  year={2025},
  note={\\url{https://github.com/kod5kod/MixTaBank}}
}
```
"""
    with open(os.path.join(WIKI_DIR, "Contributing-Guide.md"), "w") as f:
        f.write(contrib_content)

    sidebar_content = """## MixTaBank
- [[Home]]
- [[Installation & Setup|Installation-&-Setup]]
- [[CLI Downloader Guide|CLI-Downloader-Guide]]
- [[Python API Reference|Python-API-Reference]]
- [[Contributing Guide|Contributing-Guide]]

### Datasets
"""
    return sidebar_content

def generate_dataset_page(ds_key, ds_info, source, f_sidebar):
    title = ds_info.get("name", ds_key)
    filename = f"Dataset:-{ds_key}.md"
    f_sidebar.write(f"- [[{title}|Dataset:-{ds_key}]]\n")
    
    types = ds_info.get("types", {})
    shape = ds_info.get("shape", [0, 0])
    
    content = f"""# {title}

**Source:** {source.capitalize()}
**Prediction Task:** `{ds_info.get("prediction_task")}`
**Target Column:** `{ds_info.get("target_col")}`

## Schema & Dimensions
- **Rows:** {shape[0]}
- **Columns:** {shape[1]}
- **Total Cardinality:** {ds_info.get("total_cardinality", "N/A")}

### Column Types Breakdown
- **Integer Columns:** {types.get("intCols", 0)}
- **Float Columns:** {types.get("floatCols", 0)}
- **Boolean/Binary Columns:** {types.get("bool/binCols", types.get("boolCols", 0))}
- **Categorical (Multi-class):** {types.get("multi-classCols", types.get("catCols", 0))}

## Usage Example

### CLI
```bash
python download_dataset.py --name {ds_key} --source {source} --output-dir ./data/{ds_key} --format parquet
```

### Python API
```python
import mixtabank

dataset, var_types, target_col, prediction_task, metadata = mixtabank.dataset_loader(
    name="{ds_key}", source="{source}", df_type="polars"
)
```
"""
    with open(os.path.join(WIKI_DIR, filename), "w") as f:
        f.write(content)

def main():
    if os.path.exists(WIKI_DIR):
        shutil.rmtree(WIKI_DIR)
        
    run_cmd(["git", "clone", WIKI_REPO_URL, WIKI_DIR])
    
    sidebar_base = generate_core_pages()
    
    with open(os.path.join(WIKI_DIR, "_Sidebar.md"), "w") as f_sidebar:
        f_sidebar.write(sidebar_base)
        
        with open(UCI_JSON, "r") as f:
            uci_data = json.load(f)
            f_sidebar.write("\n#### UCI Datasets\n")
            for key, info in uci_data.items():
                generate_dataset_page(key, info, "uci", f_sidebar)
                
        with open(KAGGLE_JSON, "r") as f:
            kaggle_data = json.load(f)
            f_sidebar.write("\n#### Kaggle Datasets\n")
            for key, info in kaggle_data.items():
                generate_dataset_page(key, info, "kaggle", f_sidebar)

    run_cmd(["git", "add", "."], cwd=WIKI_DIR)
    
    # Check if there are changes
    status_result = subprocess.run(["git", "status", "--porcelain"], cwd=WIKI_DIR, capture_output=True, text=True)
    if not status_result.stdout.strip():
        print("No changes to commit.")
        return
        
    run_cmd(["git", "commit", "-m", "docs: Generate extensive wiki documentation"], cwd=WIKI_DIR)
    run_cmd(["git", "push"], cwd=WIKI_DIR)
    print("Wiki successfully updated!")

if __name__ == "__main__":
    main()
