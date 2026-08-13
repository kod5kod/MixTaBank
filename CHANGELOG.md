# Changelog

## 📌 0.05
* Polars-only internals (removed pandas dependencies from core).
* Introduced `Dataset` dataclass wrapping data and metadata.
* Curated markdown JSON recipe support via `--curated`.
* Upgraded `download_dataset.py` for mass downloading, auto-folder structuring, and `info.json` auto-generation.

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
