import polars as pl
from polars.testing import assert_frame_equal
import pytest
from mixtabank.src.splits import train_valid_test_split

def test_train_valid_test_split_basic():
    df = pl.DataFrame({"A": range(100)})
    train, valid, test = train_valid_test_split(df, splits=[0.5, 0.3, 0.2], seed=42)
    assert train.height == 50
    assert valid.height == 30
    assert test.height == 20
    assert train.height + valid.height + test.height == 100

def test_train_valid_test_split_determinism():
    df = pl.DataFrame({"A": range(50)})
    t1, v1, test1 = train_valid_test_split(df, splits=[0.6, 0.2, 0.2], seed=123)
    t2, v2, test2 = train_valid_test_split(df, splits=[0.6, 0.2, 0.2], seed=123)
    
    assert_frame_equal(t1, t2)
    assert_frame_equal(v1, v2)
    assert_frame_equal(test1, test2)

def test_train_valid_test_split_edge_cases():
    # Empty dataframe
    df = pl.DataFrame(schema={"A": pl.Int64})
    train, valid, test = train_valid_test_split(df, splits=[0.7, 0.15, 0.15])
    assert train.height == 0
    assert valid.height == 0
    assert test.height == 0
    
    # Truncation boundary checking (fractions that don't yield perfect integers)
    df2 = pl.DataFrame({"A": range(33)})
    t, v, te = train_valid_test_split(df2, splits=[0.7, 0.15, 0.15])
    assert t.height == int(33 * 0.7)
    assert v.height == int(33 * 0.85) - int(33 * 0.7)
    assert te.height == 33 - int(33 * 0.85)
    
    # 100% train split
    t3, v3, te3 = train_valid_test_split(df2, splits=[1.0, 0.0, 0.0])
    assert t3.height == 33
    assert v3.height == 0
    assert te3.height == 0
