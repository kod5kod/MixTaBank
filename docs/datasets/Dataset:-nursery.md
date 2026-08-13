# Nursery

**Source:** Uci
**Prediction Task:** `multi_class_classification`
**Target Column:** `class`

## Schema & Dimensions
- **Rows:** 12960
- **Columns:** 9
- **Total Cardinality:** 32

### Column Types Breakdown
- **Integer Columns:** 0
- **Float Columns:** 0
- **Boolean/Binary Columns:** 1
- **Categorical (Multi-class):** 8

## Usage Example

### CLI
```bash
python download_dataset.py --names nursery --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="nursery", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "parents": "Utf8",
    "has_nurs": "Utf8",
    "form": "Utf8",
    "children": "Utf8",
    "housing": "Utf8",
    "finance": "Utf8",
    "social": "Utf8",
    "health": "Utf8",
    "class": "Utf8"
  },
  "drop_nulls": true
}
```
