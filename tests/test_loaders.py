import polars as pl
import pytest
from mixtabank.src.loaders import _apply_recipe, Dataset

def test_apply_recipe_full():
    df = pl.DataFrame({
        "col_drop": [1, 2, 3],
        "col_keep": [4, 5, 6],
        "col_cast": ["1.1", "2.2", "3.3"],
        "col_null": [1, None, 3]
    })
    
    recipe = {
        "select_columns": ["col_drop", "col_keep", "col_cast", "col_null"],
        "drop_columns": ["col_drop"],
        "cast_types": {"col_cast": "Float64"},
        "drop_nulls": True
    }
    
    res = _apply_recipe(df, recipe)
    assert "col_drop" not in res.columns
    assert "col_keep" in res.columns
    assert res.schema["col_cast"] == pl.Float64
    assert res.height == 2  # dropped null row
    assert res["col_null"].to_list() == [1, 3]

def test_apply_recipe_empty_and_missing_keys():
    df = pl.DataFrame({"A": [1, 2, 3]})
    
    # Empty recipe should return same df without failure
    res = _apply_recipe(df, {})
    assert res.height == 3
    assert "A" in res.columns
    
def test_apply_recipe_invalid_cast():
    df = pl.DataFrame({"A": ["abc"]})
    # If the datatype is not in `pl`, the recipe parser ignores it gracefully.
    recipe = {"cast_types": {"A": "NonExistentType"}}
    res = _apply_recipe(df, recipe)
    assert res.schema["A"] == pl.Utf8

def test_dataset_dataclass():
    df = pl.DataFrame({"target": [1, 0, 1]})
    ds = Dataset(data=df, target_col="target", prediction_task="binary", metadata={"desc": "test"})
    
    assert ds.prediction_task == "binary"
    assert ds.metadata["desc"] == "test"
    
    # Test pandas conversion at API boundary
    pd_df = ds.to_pandas()
    import pandas as pd
    assert isinstance(pd_df, pd.DataFrame)
    assert list(pd_df.columns) == ["target"]

def test_apply_recipe_regex():
    df = pl.DataFrame({
        "diag": ["250.01", "V123", "250.0", "E456", "300"],
        "price": ["$100.50", "€200", "$50.00", "free", "$30"]
    })
    
    recipe = {
        "filter_regex": {
            "diag": r"^\d+(\.\d+)?$"
        },
        "replace_regex": {
            "diag": {r"\.\d+$": ""},
            "price": {r"^\$": ""}
        }
    }
    
    res = _apply_recipe(df, recipe)
    
    # filter_regex should drop "V123", "E456"
    assert res.height == 3
    
    # replace_regex should drop the .xx decimals from diag and $ from price
    assert res["diag"].to_list() == ["250", "250", "300"]
    assert res["price"].to_list() == ["100.50", "50.00", "30"]
