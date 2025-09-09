
import polars as pl


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
    print(f"Number of numerical columns: {len(df_numCols)}: {df_numCols}")
    print(f"  - Integer columns: {len(df_intCols)}: {df_intCols}")
    print(f"  - Float columns: {len(df_floatCols)}: {df_floatCols}")
   
    print(f"Number of categorical columns: {len(df_catCols)}: {df_catCols}")
    print(f"  - Binary columns: {len(df_binCols)}: {df_binCols}")
    print(f"  - Boolean columns: {len(df_boolCols)}: {df_boolCols}")
    print(f"Total categorical cardinality: {df_total_cardinality}")
    missing_cols = sum(1 for v in df_nulls.values() if v > 0)
    print(f"Columns with missing values: {missing_cols}")

    return {
        "dtypes": df_dtype,
        "shape": df_shape,
        "numCols": df_numCols,
        "numColsTotal": len(df_numCols),
        "catCols": df_catCols,
        "catColsTotal": len(df_catCols),
        "cardinality": df_cardinality,
        "total_cardinality": df_total_cardinality,
        "nulls": df_nulls,
        "missing_pct": df_missing_pct,
        "numeric_stats": numeric_stats,
        "top_unique": df_top_unique,
    }