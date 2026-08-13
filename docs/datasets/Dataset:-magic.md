# Magic Gamma Telescope Data

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `class`

## Schema & Dimensions
- **Rows:** 19020
- **Columns:** 11
- **Total Cardinality:** 0

### Column Types Breakdown
- **Integer Columns:** 0
- **Float Columns:** 10
- **Boolean/Binary Columns:** 1
- **Categorical (Multi-class):** 0

## Usage Example

### CLI
```bash
python download_dataset.py --names magic --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="magic", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "class": "Utf8"
  },
  "drop_nulls": true
}
```
