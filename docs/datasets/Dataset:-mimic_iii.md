# MIMIC-III Clinical Dataset Tabular Data Only

**Source:** Kaggle
**Prediction Task:** `multi-class_classification`
**Target Column:** `DISCHARGE_LOCATION`

## Schema & Dimensions
- **Rows:** 733
- **Columns:** 4
- **Total Cardinality:** 259

### Column Types Breakdown
- **Integer Columns:** 2
- **Float Columns:** 0
- **Boolean/Binary Columns:** 0
- **Categorical (Multi-class):** 2

## Usage Example

### CLI
```bash
python download_dataset.py --names mimic-iii --source kaggle --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="mimic_iii", source="kaggle", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "ICD9_CODE": "Utf8"
  },
  "drop_nulls": true
}
```
