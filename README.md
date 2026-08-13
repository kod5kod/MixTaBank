# 🗄️ MixTaBank: A curated collection of Heterogeneous Mixed-type Tabular Datasets  

---

## 🔍 Overview

**MixTaBank** is a collection of heterogeneous mixed-type tabular datasets tailored for evaluating tabular generative models under realistic, human-centric conditions. Designed for both academic researchers and professional practitioners, this repository provides optimized, ready-to-use tabular data.

### ✨ Features
- A curated set of real-world datasets from UCI, Kaggle, and other sources.
- Datasets varying in size, complexity, heterogeneity, and cardinality.
- Optimized support for both **Polars** and **Pandas** dataframes.
- Included utility scripts for data preparation, train/val/test splitting, and type conversion.
- Easy integration into modern data pipelines and machine learning workflows.
- Extensible API and CLI tools to quickly fetch and format data.

---

## 📦 Installation

This project uses `uv` for lightning-fast dependency and environment management.

```bash
git clone https://github.com/kod5kod/MixTaBank.git
cd MixTaBank

# Create a virtual environment and install all dependencies (including dev)
uv sync

# Activate the environment
source .venv/bin/activate    # for mac/linux
.\.venv\Scripts\activate     # for windows

# iPython kernel support (optional):
ipython kernel install --user --name=mixtabank
```

---

## 🛠️ CLI Dataset Downloader

MixTaBank includes a convenient CLI script, `download_dataset.py`, to fetch datasets, perform splits, and save the data in optimized formats (Parquet or CSV) without writing code. It also generates a comprehensive `dataset_info.json` file.

### Usage
```bash
python download_dataset.py --names <dataset_name> --output-dir <directory> [OPTIONS]
```

### Options:
- `--names`: One or more dataset names (e.g., `adult_census`).
- `--all`: Download all available datasets for the source.
- `--output-dir`: **(Required)** Directory to save the dataset subfolders.
- `--source`: Source of the dataset (`uci` or `kaggle`). Default: `uci`.
- `--format`: Format to save the dataset (`parquet` or `csv`). Default: `parquet`.
- `--curated`: Apply curated preprocessing recipes (if available).
- `--split`: Train, Valid, Test split fractions. Default: `0.7 0.15 0.15`.
- `--no-split`: Flag to download the entire dataset without splitting.
- `--seed`: Random seed for splitting. Default: `420`.

### Example
```bash
python download_dataset.py --names bank_marketing --output-dir ./data --format parquet --curated
```
This will download the `bank_marketing` dataset, apply its curated recipe, split it into train, valid, and test sets, and save them as `.parquet` files alongside an `info.json` in `./data/bank_marketing/`.

---

## 🧪 Quick Start (Python API)

You can import functions directly from the `mixtabank` module:

```python
import mixtabank

# Review available curated datasets:
print(mixtabank.uci_dict.keys())
print(mixtabank.kaggle_dict.keys())

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
ds = mixtabank.dataset_loader(
    name="adult_census", source="uci", curated=True
)

# Access the Polars dataframe or convert to pandas
polars_df = ds.data
pandas_df = ds.to_pandas()

# Get a detailed info summary dictionary
info_dict = mixtabank.get_df_info(polars_df)

# Split into train, valid, and test sets deterministically
train, valid, test = mixtabank.train_valid_test_split(polars_df, splits=[0.7, 0.15, 0.15], seed=420)

# Generate a unified info.json dictionary
info_json = mixtabank.generate_dataset_info_json(
    df=polars_df,
    name="adult_census",
    prediction_task=ds.prediction_task,
    target_col=ds.target_col,
    splits_sizes=(train.height, valid.height, test.height)
)
```

---

## 📁 Original Datasets Guide (Raw)

These are the theoretical dimensions of the datasets exactly as they appear on UCI/Kaggle prior to any processing.

| # | Dataset name | Source | Prediction Task | Target | # Rows | # Columns | # Num Features | # Cat Features | # Total Cardinality |
| -- | ------------- | ------ | --------------- | ------ | ------ | --------- | -------------- | -------------- | ------------------- |
| 1 | `taiwanese_bankruptcy` | UCI | Binary Classification | `Bankrupt?` | 6,819 | 95 | 93 | 2 | 4 |
| 2 | `support2` | UCI | Binary Classification | `death` | 9,105 | 45 | 37 | 8 | 38 |
| 3 | `nursery` | UCI | Multiclass Classification | `class` | 12,960 | 9 | 0 | 9 | 32 |
| 4 | `petfinder_tab` | Kaggle | Binary Classification | `adopted` | 14,993 | 18 | 17 | 1 | 208 |
| 5 | `magic` | Kaggle | Binary Classification | `class` | 19,020 | 11 | 10 | 1 | 2 |
| 6 | `credit_default_taiwan` | UCI | Binary Classification | `default` | 30,000 | 24 | 20 | 4 | 15 |
| 7 | `beijing_pm25` | UCI | Regression | `pm2.5` | 43,824 | 11 | 11 | 0 | 4 |
| 8 | `bank_marketing` | UCI | Binary Classification | `y` | 45,211 | 17 | 7 | 10 | 46 |
| 9 | `adult_census` | UCI | Binary Classification | `high_income` | 48,842 | 15 | 6 | 9 | 107 |
| 10 | `apartment_rent_classified` | UCI | Regression | `square_feet, price` | 99,826 | 14 | 4 | 10 | 4 |
| 11 | `diabetes_130us` | UCI | Binary Classification | `readmitted` | 101,766 | 48 | 11 | 37 | 2,462 |
| 12 | `home_credit` | Kaggle | Binary Classification | `TARGET` | 210,201 | 17 | 5 | 12 | 121 |
| 13 | `cdc_diabetes` | UCI | Binary Classification | `Diabetes_binary` | 253,680 | 22 | 7 | 15 | 44 |
| 14 | `mimic_iii` | Kaggle | Multiclass Classification | `DISCHARGE_LOCATION` | 556,617 | 11 | 2 | 9 | 850 |
| 15 | `covertype` | UCI | Multiclass Classification | `Cover_Type` | 581,012 | 55 | 11 | 44 | 93 |
| 16 | `criteo_1m` | Kaggle | Binary Classification | `target` | 1,000,000 | 40 | 13 | 27 | 14,244 |

---

## 🗃️ Curated Datasets Guide (Cleaned)

These are the exact dimensions of the datasets *after* applying MixTaBank's default Polars recipes (nulls dropped, columns correctly cast, and irrelevant features dropped).

| # | Dataset name | Source | Prediction Task | Target | # Rows | # Columns | # Num Features | # Cat Features | # Total Cardinality |
| -- | ------------- | ------ | --------------- | ------ | ------ | --------- | -------------- | -------------- | ------------------- |
| 1 | `taiwanese_bankruptcy` | UCI | Binary Classification | `Bankrupt?` | 6,819 | 94 | 92 | 2 | 4 |
| 2 | `support2` | UCI | Binary Classification | `death` | 7,816 | 30 | 20 | 10 | 38 |
| 3 | `nursery` | UCI | Multiclass Classification | `class` | 12,960 | 9 | 0 | 9 | 32 |
| 4 | `petfinder_tab` | Kaggle | Binary Classification | `adopted` | 14,976 | 18 | 11 | 7 | 208 |
| 5 | `magic` | Kaggle | Binary Classification | `class` | 19,020 | 11 | 10 | 1 | 2 |
| 6 | `credit_default_taiwan` | UCI | Binary Classification | `default` | 30,000 | 24 | 20 | 4 | 15 |
| 7 | `beijing_pm25` | UCI | Regression | `pm2.5` | 41,757 | 11 | 10 | 1 | 4 |
| 8 | `bank_marketing` | UCI | Binary Classification | `y` | 43,193 | 15 | 7 | 8 | 46 |
| 9 | `adult_census` | UCI | Binary Classification | `high_income` | 47,621 | 15 | 6 | 9 | 107 |
| 10 | `apartment_rent_classified`| UCI | Regression | `square_feet, price` | 99,826 | 14 | 4 | 10 | 4 |
| 11 | `diabetes_130us` | UCI | Binary Classification | `readmitted` | 89,782 | 43 | 11 | 32 | 1,972 |
| 12 | `home_credit` | Kaggle | Binary Classification | `TARGET` | 210,201 | 17 | 4 | 13 | 123 |
| 13 | `cdc_diabetes` | UCI | Binary Classification | `Diabetes_binary` | 253,680 | 22 | 5 | 17 | 44 |
| 14 | `mimic_iii` | Kaggle | Multiclass Classification | `DISCHARGE_LOCATION` | 556,617 | 11 | 2 | 9 | 850 |
| 15 | `covertype` | UCI | Multiclass Classification | `Cover_Type` | 581,012 | 55 | 11 | 44 | 93 |
| 16 | `criteo_1m` | Kaggle | Binary Classification | `target` | 959,140 | 17 | 5 | 12 | 14,244 |

---

## 📚 Citation

If you use this library or benchmark in your work, please cite.

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
