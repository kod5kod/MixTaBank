# Criteo Ad Click Prediction (1M rows)

**Source:** Kaggle
**Prediction Task:** `binary_classification`
**Target Column:** `target`

## Schema & Dimensions
- **Rows:** 1000000
- **Columns:** 40
- **Total Cardinality:** N/A

### Column Types Breakdown
- **Integer Columns:** 13
- **Float Columns:** 0
- **Boolean/Binary Columns:** 1
- **Categorical (Multi-class):** 26

## Usage Example

### CLI
```bash
python download_dataset.py --names criteo-1m --source kaggle --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="criteo_1m", source="kaggle", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "select_columns": [
    "target",
    "intCol_1",
    "intCol_6",
    "intCol_7",
    "intCol_8",
    "intCol_10",
    "catCol_0",
    "catCol_1",
    "catCol_4",
    "catCol_7",
    "catCol_8",
    "catCol_10",
    "catCol_12",
    "catCol_13",
    "catCol_16",
    "catCol_17",
    "catCol_22"
  ],
  "cast_types": {
    "target": "String"
  },
  "drop_nulls": true
}
```
