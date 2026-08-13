# Home Credit Default Risk

**Source:** Kaggle
**Prediction Task:** `binary_classification`
**Target Column:** `TARGET`

## Schema & Dimensions
- **Rows:** 210201
- **Columns:** 17
- **Total Cardinality:** 121

### Column Types Breakdown
- **Integer Columns:** 1
- **Float Columns:** 4
- **Boolean/Binary Columns:** 3
- **Categorical (Multi-class):** 9

## Usage Example

### CLI
```bash
python download_dataset.py --names home-credit --source kaggle --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="home_credit", source="kaggle", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "TARGET": "Utf8",
    "AMT_INCOME_TOTAL": "Int64",
    "AMT_GOODS_PRICE": "Int64"
  },
  "select_columns": [
    "NAME_CONTRACT_TYPE",
    "CODE_GENDER",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",
    "NAME_TYPE_SUITE",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE",
    "WEEKDAY_APPR_PROCESS_START",
    "ORGANIZATION_TYPE",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "TARGET"
  ],
  "drop_nulls": true
}
```
