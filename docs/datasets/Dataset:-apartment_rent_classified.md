# Apartment Rent Classified

**Source:** Uci
**Prediction Task:** `regression`
**Target Column:** `['square_feet', 'price']`

## Schema & Dimensions
- **Rows:** 99826
- **Columns:** 14
- **Total Cardinality:** 4

### Column Types Breakdown
- **Integer Columns:** 2
- **Float Columns:** 2
- **Boolean/Binary Columns:** 0
- **Categorical (Multi-class):** 10

## Usage Example

### CLI
```bash
python download_dataset.py --names apartment_rent_classified --source uci --output-dir ./data --format parquet
```

### Python API
```python
import mixtabank

# Load a dataset using the new Polars-only loader (returns a Dataset dataclass)
# (Also uses curated=True to apply any JSON recipes automatically)
dataset = mixtabank.dataset_loader(
    name="apartment_rent_classified", source="uci", curated=True
)

# Access the raw Polars DataFrame
df = dataset.data
```
