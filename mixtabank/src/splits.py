import polars as pl
from typing import Tuple, List

def train_valid_test_split(data: pl.DataFrame, splits: List[float] = [0.7, 0.15, 0.15], seed: int = 420) -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """Splits the polars dataset into training, validation, and testing sets.

    Args:
        data (pl.DataFrame): The input dataset.
        splits (list): Train, valid, test fractions.
        seed (int): Random seed for reproducibility.

    Returns:
        tuple: A tuple containing the training, validation, and testing datasets.
    """
    # Set random seed for reproducibility natively in Polars
    try:
        pl.Config.set_random_seed(seed)
    except AttributeError:
        # Fallback for older Polars versions that don't have set_random_seed
        pass

    # Split the data into train, valid, and test sets
    # Explicitly enforce shuffle=True to guarantee deterministic row randomization when fraction=1.0
    data_shuffled = data.sample(fraction=1.0, shuffle=True, seed=seed).with_row_index()

    train_frac, valid_frac, test_frac = splits
    n_rows = data_shuffled.height

    train_end = int(n_rows * train_frac)
    valid_end = int(n_rows * (train_frac + valid_frac))

    train_ids = data_shuffled.filter(pl.col("index") < train_end).drop("index")
    valid_ids = data_shuffled.filter((pl.col("index") >= train_end) & (pl.col("index") < valid_end)).drop("index")
    test_ids = data_shuffled.filter(pl.col("index") >= valid_end).drop("index")

    return train_ids, valid_ids, test_ids
