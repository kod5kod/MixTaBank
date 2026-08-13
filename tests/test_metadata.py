import polars as pl
import pytest
from mixtabank.src.metadata import get_df_info, get_metadata, generate_dataset_info_json

def test_get_df_info_basic():
    df = pl.DataFrame({
        "A": [1, 2, 3],
        "B": ["a", "b", "c"],
        "C": [1.1, 2.2, 3.3]
    })
    info = get_df_info(df)
    assert info["shape"] == (3, 3)
    assert info["numColsTotal"] == 2
    assert info["catColsTotal"] == 1
    assert info["nulls"] == {"A": 0, "B": 0, "C": 0}

def test_get_df_info_edge_cases():
    # Empty DataFrame
    df_empty = pl.DataFrame(schema={"A": pl.Int64, "B": pl.Utf8})
    info = get_df_info(df_empty)
    assert info["shape"] == (0, 2)
    assert info["nulls"]["A"] == 0
    assert info["numeric_stats"]["A"]["mean"] is None

    # Nulls only
    df_nulls = pl.DataFrame({"A": [None, None], "B": pl.Series([None, None], dtype=pl.Utf8)})
    info = get_df_info(df_nulls)
    assert info["nulls"]["A"] == 2
    assert info["numeric_stats"]["A"]["mean"] is None

    # Boolean and single cardinality
    df_bool = pl.DataFrame({"A": [True, True, False]})
    info = get_df_info(df_bool)
    assert info["boolColsTotal"] == 1

def test_get_metadata_basic():
    df = pl.DataFrame({
        "int_col": [1, 2, 3],
        "bin_cat": ["Y", "N", "N"],
        "multi_cat": ["A", "B", "C"]
    })
    meta = get_metadata(df)
    assert meta["fields"]["int_col"]["type"] == "numerical"
    assert meta["fields"]["int_col"]["subtype"] == "int"
    assert meta["fields"]["bin_cat"]["type"] == "categorical"
    assert meta["fields"]["bin_cat"]["subtype"] == "binary"
    assert meta["fields"]["multi_cat"]["type"] == "categorical"
    assert meta["fields"]["multi_cat"]["subtype"] == "multi"

def test_get_metadata_unsupported_type(capsys):
    from datetime import time
    df = pl.DataFrame({"time_col": [time(10, 0)]})
    meta = get_metadata(df)
    captured = capsys.readouterr()
    assert "Didn't match on any data type for column" in captured.out
    assert "time_col" not in meta["fields"]

def test_generate_dataset_info_json():
    df = pl.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    # With splits (using fractions as expected by the framework)
    info1 = generate_dataset_info_json(df, "data1", "regression", "A", (0.5, 0.5, 0.0))
    assert info1["train_size"] == 1
    assert info1["val_size"] == 1
    
    # Without splits
    info2 = generate_dataset_info_json(df, "data2", "regression", "A")
    assert info2["train_size"] == 2
    assert info2["val_size"] == 0
    assert info2["test_size"] == 0
