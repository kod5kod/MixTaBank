# 🗄️ MixTaBank: A curated collection of Heterogeneous Mixed-type Tabular Datasets  

---

## 🔍 Overview

**MixTaBank** is a collection of heterogeneous mixed-type tabular datasets tailored for evaluating tabular generative models under realistic, human-centric conditions. Designed for both academic researchers and professional practitioners, this repository provides optimized, ready-to-use tabular data.

### ✨ Features
- A curated set of real-world datasets from UCI and Kaggle.
- Datasets varying in size, complexity, heterogeneity, and cardinality.
- Optimized support for both **Polars** and **Pandas** dataframes.
- Included utility scripts for data preparation, train/val/test splitting, and type conversion.
- Easy integration into modern data pipelines and machine learning workflows.
- Extensible API and CLI tools to quickly fetch and format data.

---

## 📦 Installation

```bash
git clone https://github.com/kod5kod/MixTaBank.git
cd MixTaBank

# Conda Env:
conda create -n mixtabank python=3.13
conda activate mixtabank
pip install -r requirements.txt

# Python's virtualenv:
virtualenv -p python3.13 mixtabank 
source mixtabank/bin/activate    # for mac/linux  
.\mixtabank\Scripts\activate   # for windows    
pip install -r requirements.txt

# iPython kernel support (optional):
ipython kernel install --user --name=mixtabank
```

---

## 🛠️ CLI Dataset Downloader

MixTaBank includes a convenient CLI script, `download_dataset.py`, to fetch datasets, perform splits, and save the data in optimized formats (Parquet or CSV) without writing code. It also generates a comprehensive `dataset_info.json` file.

### Usage
```bash
python download_dataset.py --name <dataset_name> --output-dir <directory> [OPTIONS]
```

### Options:
- `--name`: **(Required)** The name of the dataset (e.g., `adult-census`).
- `--output-dir`: **(Required)** Directory to save the dataset and info JSON.
- `--source`: Source of the dataset (`uci` or `kaggle`). Default: `uci`.
- `--format`: Format to save the dataset (`parquet` or `csv`). Default: `parquet`.
- `--df-type`: Internal dataframe type (`polars` or `pandas`). Default: `polars`.
- `--split`: Train, Valid, Test split fractions. Default: `0.7 0.15 0.15`.
- `--no-split`: Flag to download the entire dataset without splitting.
- `--seed`: Random seed for splitting. Default: `420`.

### Example
```bash
python download_dataset.py --name bank-marketing --output-dir ./data/bank --format parquet
```
This will download the `bank-marketing` dataset, split it into train, valid, and test sets, and save them as `.parquet` files alongside a `dataset_info.json`.

---

## 🧪 Quick Start (Python API)

You can import functions directly from the `mixtabank` module:

```python
import mixtabank

# Review available curated datasets:
print(mixtabank.uci_dict.keys())
print(mixtabank.kaggle_dict.keys())

# Load a UCI dataset into a Polars DataFrame
dataset, var_types, target_col, prediction_task, metadata = mixtabank.dataset_loader(
    name="adult-census", source="uci", df_type="polars"
)

# Get a detailed info summary dictionary
# For Polars:
info_dict = mixtabank.get_df_info_pl(dataset)
# For Pandas:
# info_dict = mixtabank.get_df_info_pd(dataset)

# Split into train, valid, and test sets
train, valid, test = mixtabank.pl_train_valid_test_split(dataset, splits=[0.7, 0.15, 0.15], seed=42)

# Generate a unified dataset_info.json dictionary
info_json = mixtabank.generate_dataset_info_json(
    df=dataset,
    name="adult-census",
    prediction_task=prediction_task,
    target_col=target_col,
    splits_sizes=(train.height, valid.height, test.height)
)
```

---

## 📁 Dataset Guide

| # | Dataset name | Description | Format | Source | Link | Prediction Task | Target | # Rows | # Columns | # Num Features | # Cat Features | # Total Cardinality |
| -- | ---------------- | ----------------------------- | -------- | -------- | ---- | --------------- | ------ | ------ | --------- | -------------- | -------------- | ----------- | 
| 1 | `taiwanese_bankruptcy` | Taiwanese Bankruptcy Prediction | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction) | Binary Classification | `Bankrupt?` | 6,819 | 95 | 93 | 2 | 4 |
| 2 | `support2` | Critically ill hospitalized patient records | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/880/support2) | Binary Classification | `death` | 9,105 | 45 | 37 | 8 | 38 |
| 3 | `nursery` | Rank applications for nursery schools | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/76/nursery) | Multiclass Classification | `class` | 12,960 | 9 | 0 | 9 | 32 |
| 4 | `petfinder-tab` | Pet adoption data - tabular only | CSV | Kaggle | [link](https://www.kaggle.com/competitions/petfinder-adoption-prediction/data) | Binary/multiclass Classification | `is_adopted` | 14,993 | 18 | 11 | 7 | 208 |
| 5 | `magic` | Magic Gamma Telescope Data | CSV | Kaggle | [link](https://archive.ics.uci.edu/dataset/159/magic+gamma+telescope) | Binary | `class` | 19,020 | 11 | 10 | 1 | 2 |
| 6 | `credit-defualt-taiwan`| Default of Credit Card Clients | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) | Binary Classification | `Y` | 30,000 | 24 | 20 | 4 | 15 |
| 7 | `beijing` | Beijing PM2.5 Data | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/381/beijing+pm2+5+data) | Regression | `pm2.5` | 41,757 | 11 | 10 | 1 | 4 |
| 8 | `bank-marketing` | Bank marketing data | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/222/bank+marketing) | Binary Classification | `y` | 45,211 | 17 | 7 | 11 | 46 |
| 9 | `adult-census` | Classic UCI census dataset | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/2/adult) | Binary Classification | `is_high_income` | 48,842 | 15 | 6 | 9 | 107 | 
| 10 | `apartment_rent_classified`| Apartment Rent Classified | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified) | Regression | `square_feet`, `price` | 99,826 | 14 | 4 | 10 | 4 |
| 11 | `diabetes_130us` | Diabetes 130-US hospitals (1999-2008) | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008) | Multiclass Classification | `readmitted` | 101,766 | 48 | 11 | 35 | 2,462 |
| 12 | `home-credit` | Home Credit Default Risk | CSV | Kaggle | [link](https://www.kaggle.com/datasets/datuman/home-credit-default-risk-train-data-tabular/) | Binary Classification | `TARGET` | 210,201 | 17 | 5 | 12 | 121 |
| 13 | `cdc_diabetes` | Diabetes Health Indicators Dataset | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/891/diabetes) | Binary Classification | `Diabetes_binary` | 253,680 | 22 | 7 | 15 | 44 |
| 14 | `mimic-iii` | Critical patients care information | CSV | Kaggle | [link](https://www.kaggle.com/datasets/datuman/mimic-iii-tabular-limited-features) | Multiclass Classification | `DISCHARGE_LOCATION` | 556,617 | 11 | 2 | 9 | 850 |
| 15 | `covertype` | Forest cover types based on attributes | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/31/covertype) | Multiclass Classification | `Cover_Type` | 581,012 | 55 | 11 | 44 | 93 |
| 16 | `criteo-1m` | Criteo Ad Click Prediction (1M rows) | CSV | Kaggle | [link](https://www.kaggle.com/datasets/datuman/criteo-ad-click-limited-1m) | Binary Classification | `target` | 959,140 | 17 | 6 | 11 | 14,244 |

---

## 📚 Citation

If you use this library or benchmark in your work, please cite.

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

## Changelog

## 📌 0.04
* Added `download_dataset.py` CLI utility for downloading and splitting datasets without code.
* Exposed primary functions in root `__init__.py`.
* Added standard `pd_train_valid_test_split` for Pandas dataframe splitting.
* Added `dataset_info.json` standardized metadata generation output.

## 📌 0.03   2025-10-22
* Added Kaggle datasets walkthrough 
* Added train/test/valid splits
* Added a quick-guide 

## 📌 0.02   2025-09-14
* Added UCI datasets walkthrough 
* Added summary table
* Added `get_info` function for datasets
* Data loaded is now source agnostic
* Data loader supports `polars` and `pandas`

## 📌 0.01   2025-09-09
* Initial release
* Added UCI support
* Added UCI datasets

## 📌 0.00   2025-08-01
* Added UCI dict
* Added Kaggle support
* Added README file
