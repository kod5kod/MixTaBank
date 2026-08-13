# Bank Marketing

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `y`

## Schema & Dimensions
- **Rows:** 45211
- **Columns:** 17
- **Total Cardinality:** 46

### Column Types Breakdown
- **Integer Columns:** 7
- **Float Columns:** 0
- **Boolean/Binary Columns:** 5
- **Categorical (Multi-class):** 6

## Usage Example

### CLI
```bash
python download_dataset.py --names bank-marketing --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="bank_marketing", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "drop_columns": [
    "poutcome",
    "contact"
  ],
  "drop_nulls": true
}
```
