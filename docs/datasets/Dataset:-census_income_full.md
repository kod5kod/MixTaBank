# Census Income (KDD)

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `income`

## Schema & Dimensions
- **Rows:** 199523
- **Columns:** 42
- **Total Cardinality:** 398

### Column Types Breakdown
- **Integer Columns:** 12
- **Float Columns:** 12
- **Boolean/Binary Columns:** 2
- **Categorical (Multi-class):** 27

## Usage Example

### CLI
```bash
python download_dataset.py --names census-income_full --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="census_income_full", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "ACLSWKR": "Utf8",
    "AHGA": "Utf8",
    "AHSCOL": "Utf8",
    "AMARITL": "Utf8",
    "AMJIND": "Utf8",
    "AMJOCC": "Utf8",
    "ARACE": "Utf8",
    "AREORGN": "Utf8",
    "ASEX": "Utf8",
    "AUNMEM": "Utf8",
    "AUNTYPE": "Utf8",
    "AWKSTAT": "Utf8",
    "FILESTAT": "Utf8",
    "GRINREG": "Utf8",
    "GRINST": "Utf8",
    "HHDFMX": "Utf8",
    "HHDREL": "Utf8",
    "MIGMTR1": "Utf8",
    "MIGMTR3": "Utf8",
    "MIGMTR4": "Utf8",
    "MIGSAME": "Utf8",
    "MIGSUN": "Utf8",
    "PARENT": "Utf8",
    "PEFNTVTY": "Utf8",
    "PEMNTVTY": "Utf8",
    "PENATVTY": "Utf8",
    "PRCITSHP": "Utf8",
    "VETQVA": "Utf8",
    "income": "Utf8"
  },
  "drop_nulls": true
}
```
