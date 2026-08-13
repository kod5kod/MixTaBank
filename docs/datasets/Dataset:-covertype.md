# Covertype

**Source:** Uci
**Prediction Task:** `multi_class_classification`
**Target Column:** `Cover_Type`

## Schema & Dimensions
- **Rows:** 581012
- **Columns:** 55
- **Total Cardinality:** 93

### Column Types Breakdown
- **Integer Columns:** 11
- **Float Columns:** 0
- **Boolean/Binary Columns:** 43
- **Categorical (Multi-class):** 1

## Usage Example

### CLI
```bash
python download_dataset.py --names covertype --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="covertype", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```

## Curated Recipe

```json
{
  "cast_types": {
    "Soil_Type1": "Utf8",
    "Soil_Type2": "Utf8",
    "Soil_Type3": "Utf8",
    "Soil_Type4": "Utf8",
    "Soil_Type5": "Utf8",
    "Soil_Type6": "Utf8",
    "Soil_Type7": "Utf8",
    "Soil_Type8": "Utf8",
    "Soil_Type9": "Utf8",
    "Soil_Type10": "Utf8",
    "Soil_Type11": "Utf8",
    "Soil_Type12": "Utf8",
    "Soil_Type13": "Utf8",
    "Soil_Type14": "Utf8",
    "Soil_Type15": "Utf8",
    "Soil_Type16": "Utf8",
    "Soil_Type17": "Utf8",
    "Soil_Type18": "Utf8",
    "Soil_Type19": "Utf8",
    "Soil_Type20": "Utf8",
    "Soil_Type21": "Utf8",
    "Soil_Type22": "Utf8",
    "Soil_Type23": "Utf8",
    "Soil_Type24": "Utf8",
    "Soil_Type25": "Utf8",
    "Soil_Type26": "Utf8",
    "Soil_Type27": "Utf8",
    "Soil_Type28": "Utf8",
    "Soil_Type29": "Utf8",
    "Soil_Type30": "Utf8",
    "Soil_Type31": "Utf8",
    "Soil_Type32": "Utf8",
    "Soil_Type33": "Utf8",
    "Soil_Type34": "Utf8",
    "Soil_Type35": "Utf8",
    "Soil_Type36": "Utf8",
    "Soil_Type37": "Utf8",
    "Soil_Type38": "Utf8",
    "Soil_Type39": "Utf8",
    "Soil_Type40": "Utf8",
    "Wilderness_Area1": "Utf8",
    "Wilderness_Area2": "Utf8",
    "Wilderness_Area3": "Utf8",
    "Wilderness_Area4": "Utf8",
    "Cover_Type": "Utf8"
  },
  "drop_nulls": true
}
```
