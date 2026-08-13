# CDC Diabetes Health Indicators

**Source:** Uci
**Prediction Task:** `binary_classification`
**Target Column:** `Diabetes_binary`

## Schema & Dimensions
- **Rows:** 253680
- **Columns:** 22
- **Total Cardinality:** 30

### Column Types Breakdown
- **Integer Columns:** 7
- **Float Columns:** 0
- **Boolean/Binary Columns:** 15
- **Categorical (Multi-class):** 0

## Usage Example

### CLI
```bash
python download_dataset.py --names cdc_diabetes --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="cdc_diabetes", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "Education": "Utf8",
    "Income": "Utf8",
    "Diabetes_binary": "Utf8",
    "HighBP": "Utf8",
    "HighChol": "Utf8",
    "CholCheck": "Utf8",
    "Smoker": "Utf8",
    "Stroke": "Utf8",
    "HeartDiseaseorAttack": "Utf8",
    "PhysActivity": "Utf8",
    "Fruits": "Utf8",
    "Veggies": "Utf8",
    "HvyAlcoholConsump": "Utf8",
    "AnyHealthcare": "Utf8",
    "NoDocbcCost": "Utf8",
    "DiffWalk": "Utf8",
    "Sex": "Utf8"
  },
  "drop_nulls": true
}
```
