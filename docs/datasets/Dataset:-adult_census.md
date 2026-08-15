# Adult

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `income`

## Schema & Dimensions
- **Rows:** 48842
- **Columns:** 15
- **Total Cardinality:** 107

### Column Types Breakdown
- **Integer Columns:** 6
- **Float Columns:** 0
- **Boolean/Binary Columns:** 2
- **Categorical (Multi-class):** 7

## Usage Example

### CLI
```bash
python download_dataset.py --names adult-census --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="adult_census", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "rename_columns": {
    "income": "high_income"
  },
  "replace_values": {
    "income": {
      ">50K": "1",
      ">50K.": "1",
      "<=50K": "0",
      "<=50K.": "0"
    }
  },
  "drop_nulls": true
}
```
