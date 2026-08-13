# Beijing PM2.5 Data

**Source:** Uci
**Prediction Task:** `regression`
**Target Column:** `pm2.5`

## Schema & Dimensions
- **Rows:** 43824
- **Columns:** 11
- **Total Cardinality:** 0

### Column Types Breakdown
- **Integer Columns:** 10
- **Float Columns:** 1
- **Boolean/Binary Columns:** 0
- **Categorical (Multi-class):** 1

## Usage Example

### CLI
```bash
python download_dataset.py --names beijing_pm25 --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="beijing_pm25", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "year": "Int64",
    "month": "Int64",
    "day": "Int64",
    "hour": "Int64",
    "pm2.5": "Int64",
    "DEWP": "Int64",
    "TEMP": "Int64",
    "PRES": "Int64",
    "Is": "Int64",
    "Ir": "Int64",
    "cbwd": "Utf8"
  },
  "drop_nulls": true
}
```
