# Diabetes 130-US hospitals for years 1999-2008

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `readmitted`

## Schema & Dimensions
- **Rows:** 101766
- **Columns:** 48
- **Total Cardinality:** 2462

### Column Types Breakdown
- **Integer Columns:** 11
- **Float Columns:** 0
- **Boolean/Binary Columns:** 9
- **Categorical (Multi-class):** 26

## Usage Example

### CLI
```bash
python download_dataset.py --names diabetes_130us --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="diabetes_130us", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "drop_columns": [
    "weight",
    "payer_code",
    "medical_specialty",
    "max_glu_serum",
    "A1Cresult"
  ],
  "filter_regex": {
    "diag_1": "^\\d+(\\.\\d+)?$",
    "diag_2": "^\\d+(\\.\\d+)?$",
    "diag_3": "^\\d+(\\.\\d+)?$"
  },
  "replace_regex": {
    "diag_1": {"\\.\\d+$": ""},
    "diag_2": {"\\.\\d+$": ""},
    "diag_3": {"\\.\\d+$": ""}
  },
  "cast_types": {
    "race": "Utf8",
    "gender": "Utf8",
    "age": "Utf8",
    "diag_1": "Utf8",
    "diag_2": "Utf8",
    "diag_3": "Utf8",
    "metformin": "Utf8",
    "repaglinide": "Utf8",
    "nateglinide": "Utf8",
    "chlorpropamide": "Utf8",
    "glimepiride": "Utf8",
    "acetohexamide": "Utf8",
    "glipizide": "Utf8",
    "glyburide": "Utf8",
    "tolbutamide": "Utf8",
    "pioglitazone": "Utf8",
    "rosiglitazone": "Utf8",
    "acarbose": "Utf8",
    "miglitol": "Utf8",
    "troglitazone": "Utf8",
    "tolazamide": "Utf8",
    "examide": "Utf8",
    "citoglipton": "Utf8",
    "insulin": "Utf8",
    "glyburide-metformin": "Utf8",
    "glipizide-metformin": "Utf8",
    "glimepiride-pioglitazone": "Utf8",
    "metformin-rosiglitazone": "Utf8",
    "metformin-pioglitazone": "Utf8",
    "change": "Utf8",
    "diabetesMed": "Utf8",
    "readmitted": "Utf8"
  },
  "drop_nulls": true
}
```
