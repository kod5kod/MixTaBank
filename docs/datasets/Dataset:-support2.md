# SUPPORT2

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `death`

## Schema & Dimensions
- **Rows:** 9105
- **Columns:** 45
- **Total Cardinality:** 38

### Column Types Breakdown
- **Integer Columns:** 6
- **Float Columns:** 31
- **Boolean/Binary Columns:** 1
- **Categorical (Multi-class):** 7

## Usage Example

### CLI
```bash
python download_dataset.py --names support2 --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="support2", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "drop_columns": [
    "edu",
    "income",
    "totmcst",
    "prg2m",
    "prg6m",
    "pafi",
    "alb",
    "bili",
    "ph",
    "glucose",
    "bun",
    "urine",
    "adlp",
    "adls",
    "sfdm2"
  ],
  "cast_types": {
    "sex": "Utf8",
    "dzgroup": "Utf8",
    "dzclass": "Utf8",
    "race": "Utf8",
    "diabetes": "Utf8",
    "dementia": "Utf8",
    "ca": "Utf8",
    "dnr": "Utf8",
    "death": "Utf8",
    "hospdead": "Utf8"
  },
  "drop_nulls": true
}
```
