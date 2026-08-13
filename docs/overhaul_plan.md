# MixTaBank Framework Overhaul Plan

This document outlines the overhaul plan for the MixTaBank framework, addressing the need for a more robust, Polars-native architecture, automated data curation, and expanded datasets.

---

## Execution Scope & Phasing

The execution is split into two phases:

**Phase 1 (Immediate Execution):**
1. Generate this formal `docs/overhaul_plan.md` document.
2. Adapt and import `AGENTS.md` from the sister project into this repository.
3. Fix the train/test/valid split bug in `utils.py`.
4. Move the current `.wiki_repo/Dataset:* md` info files into a new `docs/datasets/` subfolder.

**Phase 2 (Follow-up):**
- Polars-only internals refactor.
- Implementation of the "curated recipes" feature.
- Mass download CLI/API implementation.

---

## Proposed Overhaul Details

### 1. Import and Adapt `AGENTS.md`
- Copy `AGENTS.md` into the project root.
- Adapt the Project structure, removing task-specific details from other frameworks and replacing them with `MixTaBank` context (Tabular dataset loader, Mixed-type datasets, Kaggle/UCI integration).
- Update environment settings (e.g., Python 3.13, `mixtabank` conda env).

### 2. CS and DS Review Feedback
**Computer Scientist Lens:**
- **Polars-Native Architecture**: The library's internals (loaders, splitters, metadata inspectors) will be rewritten to be **strictly Polars-only** to maximize efficiency and speed. However, to avoid limiting the end user, we will add an explicit `return_pandas=True` or `to_pandas()` API call at the boundaries.
- **Architecture**: The `dataset_loader` returns a 5-element tuple. This should be refactored into a `Dataset` dataclass for better API ergonomics.
- **Project Structure**: Files are in `mixtabank/src/utils.py`. This should be modularized (e.g., `loaders.py`, `splits.py`, `metadata.py`).
- **Dependencies**: The project lacks a `pyproject.toml` for modern packaging.

**Data Scientist Lens:**
- **Stratified Splitting**: The current `train_valid_test_split` randomly slices the data. For classification tasks, it should support **stratified splitting** to maintain target class distributions.

### 3. "Curated" Option & Recipes
- Introduce a **"curated recipe"** architecture. Each dataset will have its specific preprocessing operations (aligned with `data_loader_example.ipynb`) documented in its corresponding `.md` info file.
- The `dataset_loader` will read and execute this curated recipe. This allows the end user to easily inspect and customize the data loading transformations for each dataset.
- **Explicit Exclusion**: This curated option will **not** include complex transformations such as tokenization, target encoding, or frequency encoding. It focuses on basic operations needed for each dataset as per the notebook.

### 4. Fixing the Split Bug
- **Issue**: Polars' `sample(seed=seed)` is not always deterministic across multi-threaded executions without strict configuration. 
- **Fix**: In `pl_train_valid_test_split`, explicitly set `pl.Config.set_random_seed(seed)` (or global seed) and use `shuffle=True` or numpy to guarantee a deterministic permutation array to slice the DataFrame reliably. 

### 5. Mass Download API and CLI
- **CLI**: Update `download_dataset.py` to accept `--names` (list of datasets) or `--all` to iterate over all available datasets.
- **Python API**: Introduce `mixtabank.download_datasets(names=["adult-census", "bank-marketing"], ...)` which internally loops over the loader, splits, and saves them efficiently using Polars.

### 6. Suggested Datasets (Mixed-type, High Cardinality)
To enrich the focus on high-cardinality and mixed types, the following datasets will be added:
- **Amazon Employee Access Challenge** (Kaggle): Highly categorical, complex high-cardinality features.
- **Avazu Click-Through Rate Prediction** (Kaggle): Massive dataset with extreme cardinality categorical variables.
- **KDD Cup 1999 / NSL-KDD** (UCI): Classic mixed-type network intrusion data.
- **Santander Customer Transaction Prediction** (Kaggle): Numeric/mixed types with challenging distributions.
- **IEEE-CIS Fraud Detection** (Kaggle): Contains a wide variety of mixed types (categorical, numeric, temporal) with many high cardinality variables.
- **Criteo Display Advertising** (Kaggle): Standard benchmark for high-cardinality categorical encoding (adding the full version or variants alongside the existing `criteo-1m`).

### 7. Documentation Improvements
- Add docstrings to all exposed functions in the `__init__.py`.
- **Wiki Migration**: Move all the current `.wiki_repo/Dataset:* md` info files into a cleaner subfolder structure under `docs/datasets/`.
- Provide detailed usage examples (e.g., `quickstart.md`, `curation_guide.md`) in the `docs/` folder.
- Update `README.md` to highlight the Polars-native speed and mass download capabilities.

### 8. Other Improvements & Fixes
- **`config.toml` Integration**: Introduce a central configuration file (`configs/config.toml`) to store project-level defaults such as the global random `seed`, default `split` fractions, default list of datasets for mass download, and environment variables.
- Add a proper `pytest` suite for the loaders and splitters.
- Implement robust error handling for Kaggle API rate limits or UCI connection timeouts.

### 9. Additional Feature Suggestions (For Future Phases)
- **Local Caching System**: Implement a caching layer (e.g., `~/.cache/mixtabank/`).
- **Data Quality Validation**: Tabular data sources can sometimes change silently. We could define lightweight schemas (using `pandera` or custom Polars schema checks) to validate that the downloaded data matches the expected columns, types, and missingness bounds.
- **Fast Sub-sampling**: For massive datasets, add a `sample_size=N` argument to the loader to instantly return a smaller, representative subset.
- **Hugging Face Datasets Integration**: Add a simple `.to_hf_dataset()` method to our planned `Dataset` dataclass to make this library highly interoperable with modern ML ecosystems.
- *(Held off for later)* **K-Fold & Multi-seed Splitting**: Offering `k_fold_split` to standardize benchmarking.
