# Taiwanese Bankruptcy

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `Bankrupt?`

## Schema & Dimensions
- **Rows:** 6819
- **Columns:** 95
- **Total Cardinality:** 4

### Column Types Breakdown
- **Integer Columns:** 0
- **Float Columns:** 93
- **Boolean/Binary Columns:** 2
- **Categorical (Multi-class):** 0

## Usage Example

### CLI
```bash
python download_dataset.py --names taiwanese_bankruptcy --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="taiwanese_bankruptcy", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "drop_columns": [
    " Net Income Flag"
  ],
  "cast_types": {
    "Bankrupt?": "Utf8",
    " Liability-Assets Flag": "Utf8"
  },
  "drop_nulls": true
}
```
