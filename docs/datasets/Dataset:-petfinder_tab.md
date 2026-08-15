# Petfinder Adoption Prediction (Tabular)

**Source:** Kaggle
**Prediction Task:** `binary_classification`
**Target Column:** `y`

## Schema & Dimensions
- **Rows:** 45211
- **Columns:** 17
- **Total Cardinality:** N/A

### Column Types Breakdown
- **Integer Columns:** 7
- **Float Columns:** 10
- **Boolean/Binary Columns:** 1
- **Categorical (Multi-class):** 10

## Usage Example

### CLI
```bash
python download_dataset.py --names petfinder-tab --source kaggle --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="petfinder_tab", source="kaggle", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "rename_columns": {
    "is_adopted": "adopted"
  },
  "cast_types": {
    "is_adopted": "Utf8"
  },
  "drop_nulls": true
}
```
