import kagglehub
import pandas as pd
import polars as pl
from kagglehub import KaggleDatasetAdapter
from pandas.api import types as pdt
from ucimlrepo import fetch_ucirepo

import mixtabank


def dataset_loader(name="bank-marketing", source="uci", df_type="polars"):
    """
    Load a dataset from either the UCI Machine Learning Repository or Kaggle
    and convert it into a Polars or Pandas DataFrame.

    Parameters
    ----------
    name : str, default="bank-marketing"
        Name of the dataset to load. Must be present in the corresponding source dictionary.
    source : str, default="uci"
        Source of the dataset. Must be either 'uci' or 'kaggle'.
    df_type : str, default="polars"
        Type of DataFrame to return. Must be either 'polars' or 'pandas'.

    Returns
    -------
    dataset : pl.DataFrame or pd.DataFrame
        The loaded dataset as a Polars or Pandas DataFrame.
    target_col_name : str
        The name of the target column for prediction.
    prediction_task : str
        The type of prediction task (e.g., 'binary_classification', 'regression').

    Raises
    ------
    ValueError
        If the dataset name is not found, the source is invalid, or df_type is invalid.
    """
    if source == "uci":
        try:
            uci_data = fetch_ucirepo(id=mixtabank.uci_dict[name]["uci_id"])
        except KeyError:
            raise ValueError(f"Dataset '{name}' not found in the UCI dictionary.")
        # Load dataset from UCI repository into Polars/Pandas DataFrame
        if df_type == "polars":
            X = pl.from_pandas(uci_data.data.features)
            Y = pl.from_pandas(uci_data.data.targets)
            dataset = pl.concat([X, Y], how="horizontal")
        elif df_type == "pandas":
            X = uci_data.data.features
            Y = uci_data.data.targets
            dataset = pd.concat([X, Y], axis=1)
        else:
            raise ValueError("df_type must be either 'polars' or 'pandas'")
        target_col_name = mixtabank.uci_dict[name]["target_col"]
        prediction_task = mixtabank.uci_dict[name]["prediction_task"]
        var_types = {row["name"]: row["type"] for index, row in uci_data["variables"][["name", "type"]].iterrows()}
        metadata = uci_data["metadata"]
        return dataset, var_types, target_col_name, prediction_task, metadata

    elif source == "kaggle":
        dataset_path = mixtabank.kaggle_dict[name]["kaggle_path"]
        file_name = mixtabank.kaggle_dict[name]["filename"]
        # Load the file directly into a Polars DataFrame
        if df_type == "pandas":
            df = kagglehub.dataset_load(KaggleDatasetAdapter.PANDAS, dataset_path, file_name)
        elif df_type == "polars":
            df = kagglehub.dataset_load(KaggleDatasetAdapter.POLARS, dataset_path, file_name).collect()
        else:
            raise ValueError("df_type must be either 'polars' or 'pandas'")
        target_col_name = mixtabank.kaggle_dict[name]["target_col"]
        prediction_task = mixtabank.kaggle_dict[name]["prediction_task"]
        return df, None, target_col_name, prediction_task, None

    else:
        raise ValueError("Source must be either 'uci' or 'kaggle'")


def get_df_info_pl(df):
    """
    Inspect a Polars DataFrame and return a compact summary.

    Parameters
    ----------
    df : pl.DataFrame
        Input dataframe to inspect.

    Returns
    -------
    dict
        Summary containing:
        - dtypes: mapping column -> dtype (string)
        - shape: (rows, cols)
        - numCols: list of numerical column names
        - numColsTotal: number of numerical columns
        - catCols: list of categorical (string/Utf8) column names
        - catColsTotal: number of categorical columns
        - cardinality: mapping categorical column -> number of unique values
        - total_cardinality: sum of categorical cardinalities
        - nulls: mapping column -> null count
        - missing_pct: mapping column -> percent missing (0-100)
        - numeric_stats: basic stats for numerical columns (mean, std, min, median, max, missing)
        - top_unique: up to first 10 unique values for each categorical column
    """
    # column dtypes and shape
    df_dtype = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
    df_shape = df.shape

    # classify columns by dtype (treat Utf8 / String as categorical)
    df_numCols = [col for col in df.columns if df[col].dtype != pl.Utf8]
    df_catCols = [col for col in df.columns if df[col].dtype == pl.Utf8]

    # get more specific numeric and categorical types if needed
    df_intCols = [col for col in df_numCols if df[col].dtype in (pl.Int8, pl.Int16, pl.Int32, pl.Int64)]
    df_floatCols = [col for col in df_numCols if df[col].dtype in (pl.Float32, pl.Float64)]
    df_boolCols = [col for col in df_numCols if df[col].dtype == pl.Boolean]
    df_multiCatCols = [col for col in df_catCols if df[col].n_unique() > 2]
    df_binCols = [col for col in df_catCols if df[col].n_unique() == 2]

    # cardinality for categorical columns
    df_cardinality = {col: int(df[col].n_unique()) for col in df_catCols}
    df_total_cardinality = sum(df_cardinality.values())

    # missing / null information
    df_nulls = {col: int(df[col].null_count()) for col in df.columns}
    ## missing percentage
    df_missing_pct = {col: round(100 * cnt / df_shape[0], 4) for col, cnt in df_nulls.items()}

    # small sample of unique values for categorical columns (useful for quick inspection)
    df_top_unique = {col: df[col].unique().to_list()[:10] for col in df_catCols}

    # basic numeric statistics for numerical columns
    numeric_stats = {}
    for col in df_numCols:
        s = df[col]
        # compute stats safely (polars returns None for empty/na-only series)
        mean = s.mean()
        std = s.std()
        mn = s.min()
        med = s.median()
        mx = s.max()
        numeric_stats[col] = {
            "mean": float(mean) if mean is not None else None,
            "std": float(std) if std is not None else None,
            "min": float(mn) if mn is not None else None,
            "median": float(med) if med is not None else None,
            "max": float(mx) if mx is not None else None,
            "missing": int(s.null_count()),
        }

    # print a concise human-readable summary
    print(f"DataFrame shape: {df_shape}")
    print("Data types (according to dtypes):")
    print(f"Number of numerical columns: {len(df_numCols)}:\n{df_numCols}")
    print(f"  - Integer columns: {len(df_intCols)}: {df_intCols}")
    print(f"  - Float columns: {len(df_floatCols)}: {df_floatCols}")

    print(f"Number of categorical columns: {len(df_catCols)}:\n{df_catCols}")
    print(f"  - Multiclass columns: {len(df_multiCatCols)}: {df_multiCatCols}")
    print(f"  - Binary columns: {len(df_binCols)}: {df_binCols}")
    print(f"  - Boolean columns: {len(df_boolCols)}: {df_boolCols}")
    print(f"Total categorical cardinality: {df_total_cardinality}")
    print(
        f"Total types count:\ntotal numerical: {len(df_numCols)} (int: {len(df_intCols)}, float: {len(df_floatCols)}),\nTotal categorical: {len(df_catCols)} (multi-class: {len(df_multiCatCols)}, bin_cat: {len(df_binCols)}, bool_cat: {len(df_boolCols)}): "
    )
    missing_cols = sum(1 for v in df_nulls.values() if v > 0)
    print(f"Columns with missing values: {missing_cols}")

    return {
        "dtypes": df_dtype,
        "shape": df_shape,
        "numCols": df_numCols,
        "numColsTotal": len(df_numCols),
        "intCols": df_intCols,
        "intColsTotal": len(df_intCols),
        "floatCols": df_floatCols,
        "floatColsTotal": len(df_floatCols),
        "catCols": df_catCols,
        "catColsTotal": len(df_catCols),
        "binCols": df_binCols,
        "binColsTotal": len(df_binCols),
        "boolCols": df_boolCols,
        "boolColsTotal": len(df_boolCols),
        "cardinality": df_cardinality,
        "total_cardinality": df_total_cardinality,
        "nulls": df_nulls,
        "missing_pct": df_missing_pct,
        "numeric_stats": numeric_stats,
        "top_unique": df_top_unique,
    }


def get_df_info_pd(df):
    """
    Inspect a pandas DataFrame and return a compact summary.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe to inspect.

    Returns
    -------
    dict
        Summary containing:
        - dtypes: mapping column -> dtype (string)
        - shape: (rows, cols)
        - numCols: list of numerical column names
        - numColsTotal: number of numerical columns
        - catCols: list of categorical (object/Category/str) column names
        - catColsTotal: number of categorical columns
        - cardinality: mapping categorical column -> number of unique values
        - total_cardinality: sum of categorical cardinalities
        - nulls: mapping column -> null count
        - missing_pct: mapping column -> percent missing (0-100)
        - numeric_stats: basic stats for numerical columns (mean, std, min, median, max, missing)
        - top_unique: up to first 10 unique values for each categorical column
    """
    # basic dtype map and shape
    df_dtype = {col: str(df[col].dtype) for col in df.columns}
    df_shape = df.shape
    n_rows = df_shape[0]

    # classify columns: treat object and category as categorical
    df_catCols = [
        col
        for col in df.columns
        if pdt.is_string_dtype(df[col].dtype)
        or pdt.is_categorical_dtype(df[col].dtype)
        or pdt.is_object_dtype(df[col].dtype)
    ]
    # numeric includes ints, floats and booleans (match prior behavior which treated boolean among numeric-like)
    df_numCols = [col for col in df.columns if pdt.is_numeric_dtype(df[col].dtype) or pdt.is_bool_dtype(df[col].dtype)]
    # more specific numeric types
    df_intCols = [
        col for col in df_numCols if pdt.is_integer_dtype(df[col].dtype) and not pdt.is_bool_dtype(df[col].dtype)
    ]
    df_floatCols = [col for col in df_numCols if pdt.is_float_dtype(df[col].dtype)]
    df_boolCols = [col for col in df_numCols if pdt.is_bool_dtype(df[col].dtype)]
    # categorical splits
    df_cardinality = {col: int(df[col].nunique(dropna=True)) for col in df_catCols}
    df_multiCatCols = [col for col, c in df_cardinality.items() if c > 2]
    df_binCols = [col for col, c in df_cardinality.items() if c == 2]

    # missing / null information
    df_nulls = {col: int(df[col].isnull().sum()) for col in df.columns}
    if n_rows > 0:
        df_missing_pct = {col: round(100 * cnt / n_rows, 4) for col, cnt in df_nulls.items()}
    else:
        df_missing_pct = {col: None for col in df.columns}

    df_total_cardinality = sum(df_cardinality.values())

    # small sample of unique values for categorical columns
    df_top_unique = {}
    for col in df_catCols:
        vals = df[col].dropna().unique()
        try:
            df_top_unique[col] = list(vals[:10])
        except Exception:
            # fallback if unique returns non-sliceable type
            df_top_unique[col] = list(vals)[:10]

    # basic numeric statistics for numerical columns
    numeric_stats = {}
    for col in df_numCols:
        s = df[col]
        mean = s.mean()
        std = s.std()
        mn = s.min()
        med = s.median()
        mx = s.max()
        numeric_stats[col] = {
            "mean": float(mean) if pd.notna(mean) else None,
            "std": float(std) if pd.notna(std) else None,
            "min": float(mn) if pd.notna(mn) else None,
            "median": float(med) if pd.notna(med) else None,
            "max": float(mx) if pd.notna(mx) else None,
            "missing": int(s.isnull().sum()),
        }

    # print a concise human-readable summary
    print(f"DataFrame shape: {df_shape}")
    print("Data types (according to dtypes):")
    print(f"Number of numerical columns: {len(df_numCols)}:\n{df_numCols}")
    print(f"  - Integer columns: {len(df_intCols)}: {df_intCols}")
    print(f"  - Float columns: {len(df_floatCols)}: {df_floatCols}")
    print(f"Number of categorical columns: {len(df_catCols)}:\n{df_catCols}")
    print(f"  - Multiclass columns: {len(df_multiCatCols)}: {df_multiCatCols}")
    print(f"  - Binary columns: {len(df_binCols)}: {df_binCols}")
    print(f"  - Boolean columns: {len(df_boolCols)}: {df_boolCols}")
    print(f"Total categorical cardinality: {df_total_cardinality}")
    print(
        f"Total types count:\ntotal numerical: {len(df_numCols)} (int: {len(df_intCols)}, float: {len(df_floatCols)}),\nTotal categorical: {len(df_catCols)} (multi-class: {len(df_multiCatCols)}, bin_cat: {len(df_binCols)}, bool_cat: {len(df_boolCols)}): "
    )
    missing_cols = sum(1 for v in df_nulls.values() if v > 0)
    print(f"Columns with missing values: {missing_cols}")

    return {
        "dtypes": df_dtype,
        "shape": df_shape,
        "numCols": df_numCols,
        "numColsTotal": len(df_numCols),
        "intCols": df_intCols,
        "intColsTotal": len(df_intCols),
        "floatCols": df_floatCols,
        "floatColsTotal": len(df_floatCols),
        "catCols": df_catCols,
        "catColsTotal": len(df_catCols),
        "binCols": df_binCols,
        "binColsTotal": len(df_binCols),
        "boolCols": df_boolCols,
        "boolColsTotal": len(df_boolCols),
        "cardinality": df_cardinality,
        "total_cardinality": df_total_cardinality,
        "nulls": df_nulls,
        "missing_pct": df_missing_pct,
        "numeric_stats": numeric_stats,
        "top_unique": df_top_unique,
    }


def pl_train_valid_test_split(data, splits=[0.7, 0.15, 0.15], seed=420):
    """Splits the polars dataset into training, validation, and testing sets.

    Args:
        data (pl.DataFrame): The input dataset.
        seed (int): Random seed for reproducibility.

    Returns:
        tuple: A tuple containing the training, validation, and testing datasets.
    """
    # Set random seed for reproducibility
    # pl.Config.set_global_seed(seed)

    # Split the data into train, valid, and test sets

    data_shuffled = data.sample(fraction=1.0, seed=seed).with_row_index()  # Shuffle and add index

    train_frac, valid_frac, test_frac = splits
    n_rows = data_shuffled.height

    train_end = int(n_rows * train_frac)
    valid_end = int(n_rows * (train_frac + valid_frac))

    train_ids = data_shuffled.filter(pl.col("index") < train_end).drop("index")
    valid_ids = data_shuffled.filter((pl.col("index") >= train_end) & (pl.col("index") < valid_end)).drop("index")
    test_ids = data_shuffled.filter(pl.col("index") >= valid_end).drop("index")

    return train_ids, valid_ids, test_ids