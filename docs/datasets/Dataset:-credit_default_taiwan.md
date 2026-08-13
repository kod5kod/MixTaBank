# Default of Credit Card Clients

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `Y`

## Schema & Dimensions
- **Rows:** 30000
- **Columns:** 24
- **Total Cardinality:** 15

### Column Types Breakdown
- **Integer Columns:** 20
- **Float Columns:** 0
- **Boolean/Binary Columns:** 2
- **Categorical (Multi-class):** 2

## Usage Example

### CLI
```bash
python download_dataset.py --names credit-defualt-taiwan --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="credit_default_taiwan", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "rename_columns": {
    "X1": "Credit_Amount",
    "X2": "Gender",
    "X3": "Education_Level",
    "X4": "Marital_Status",
    "X5": "Age",
    "X6": "Pay_0",
    "X7": "Pay_2",
    "X8": "Pay_3",
    "X9": "Pay_4",
    "X10": "Pay_5",
    "X11": "Pay_6",
    "X12": "Bill_Amount1",
    "X13": "Bill_Amount2",
    "X14": "Bill_Amount3",
    "X15": "Bill_Amount4",
    "X16": "Bill_Amount5",
    "X17": "Bill_Amount6",
    "X18": "Pay_Amount1",
    "X19": "Pay_Amount2",
    "X20": "Pay_Amount3",
    "X21": "Pay_Amount4",
    "X22": "Pay_Amount5",
    "X23": "Pay_Amount6",
    "Y": "default"
  },
  "cast_types": {
    "X2": "Utf8",
    "X3": "Utf8",
    "X4": "Utf8",
    "Y": "Utf8"
  },
  "drop_nulls": true
}
```
