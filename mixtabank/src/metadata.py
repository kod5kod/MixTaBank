import polars as pl

def get_df_info(df: pl.DataFrame):
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
    df_missing_pct = {col: round(100 * cnt / df_shape[0], 4) if df_shape[0] > 0 else 0.0 for col, cnt in df_nulls.items()}

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


def get_metadata(dataframe: pl.DataFrame) -> dict:
    """
    Get the types metadata of a Polars dataframe.

    Args:
        dataframe (pl.DataFrame): A Polars dataframe

    Returns:
        dict: A dict with type metadata information

    Notes:
        The metadata will be a dictionary with the column name as the key and a
        dictionary with the type and subtype as the value. The type will be one
        of ['categorical', 'numerical'] and the subtype will be one of
        ['binary', 'multi'] or ['float', 'int'].
    """
    tmp = {}
    metadata = {}

    for col in dataframe.columns:
        dtype = dataframe.schema[col]
        col_data = dataframe[col].drop_nulls()

        if dtype == pl.String:
            unique_vals = col_data.unique()
            if unique_vals.len() == 2:
                tmp[col] = {"type": "categorical", "subtype": "binary"}
            else:
                tmp[col] = {"type": "categorical", "subtype": "multi"}

        elif dtype in [pl.Float32, pl.Float64]:
            tmp[col] = {"type": "numerical", "subtype": "float"}

        elif dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64]:
            tmp[col] = {"type": "numerical", "subtype": "int"}

        else:
            print(f"Didn't match on any data type for column: {col}")

    metadata["fields"] = tmp
    return metadata

def generate_dataset_info_json(df: pl.DataFrame, name: str, prediction_task: str, target_col: str, splits_sizes: tuple = None) -> dict:
    """
    Generate the standardized dataset_info JSON representation for a dataset.
    
    Parameters
    ----------
    df : pl.DataFrame
        The full dataset DataFrame.
    name : str
        The dataset name.
    prediction_task : str
        The task type (e.g., 'binary_classification', 'multiclass', 'regression').
    target_col : str
        The target column name.
    splits_sizes : tuple or list, optional
        A tuple/list of sizes (train, val, test) used for splitting.
        
    Returns
    -------
    dict
        A dictionary representation ready to be saved as info.json.
    """
    info = get_df_info(df)
    
    if splits_sizes:
        train_size = splits_sizes[0]
        val_size = splits_sizes[1] if len(splits_sizes) > 1 else 0
        test_size = splits_sizes[2] if len(splits_sizes) > 2 else 0
    else:
        train_size = df.height
        val_size = 0
        test_size = 0
        
    return {
        "name": name,
        "prediction_task": prediction_task,
        "target_col": target_col,
        "train_size": train_size,
        "val_size": val_size,
        "test_size": test_size,
        "catCols": info["catCols"],
        "intCols": info["intCols"],
        "floatCols": info["floatCols"]
    }

