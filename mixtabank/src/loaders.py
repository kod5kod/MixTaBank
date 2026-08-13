import os
import json
import re
from dataclasses import dataclass
from typing import Union, Optional, List, Dict
import polars as pl
from kagglehub import KaggleDatasetAdapter
import kagglehub
from ucimlrepo import fetch_ucirepo
import mixtabank


@dataclass
class Dataset:
    data: pl.DataFrame
    target_col: str
    prediction_task: str
    metadata: Optional[dict]

    def to_pandas(self):
        """Returns the dataset as a Pandas DataFrame for end-user flexibility."""
        return self.data.to_pandas()


def _apply_recipe(df: pl.DataFrame, recipe: dict) -> pl.DataFrame:
    """Applies a curated JSON recipe to a Polars DataFrame."""
    # 1. select_columns
    if "select_columns" in recipe:
        df = df.select(recipe["select_columns"])
        
    # 2. drop_columns
    if "drop_columns" in recipe:
        df = df.drop(recipe["drop_columns"])
    
    # 3. cast_types
    if "cast_types" in recipe:
        cast_dict = {}
        for col, dtype_str in recipe["cast_types"].items():
            if hasattr(pl, dtype_str):
                cast_dict[col] = getattr(pl, dtype_str)
        if cast_dict:
            df = df.cast(cast_dict)
            
    # 4. replace_values
    if "replace_values" in recipe:
        for col, mapping in recipe["replace_values"].items():
            df = df.with_columns(
                pl.col(col).replace(mapping)
            )
            
    # 5. rename_columns
    if "rename_columns" in recipe:
        df = df.rename(recipe["rename_columns"])
            
    # 6. filter_regex
    if "filter_regex" in recipe:
        for col, pattern in recipe["filter_regex"].items():
            df = df.filter(pl.col(col).str.contains(pattern))
            
    # 7. replace_regex
    if "replace_regex" in recipe:
        for col, mapping in recipe["replace_regex"].items():
            for pattern, replacement in mapping.items():
                df = df.with_columns(
                    pl.col(col).str.replace(pattern, replacement)
                )

    # 8. drop_nulls
    if recipe.get("drop_nulls"):
        df = df.drop_nulls()
        
    return df


def dataset_loader(name: str = "bank-marketing", source: str = "uci", curated: bool = False) -> Dataset:
    """
    Load a dataset from either the UCI Machine Learning Repository or Kaggle
    and convert it into a Polars DataFrame wrapped in a Dataset dataclass.

    Parameters
    ----------
    name : str, default="bank-marketing"
        Name of the dataset to load. Must be present in the corresponding source dictionary.
    source : str, default="uci"
        Source of the dataset. Must be either 'uci' or 'kaggle'.
    curated : bool, default=False
        If True, looks for a curated recipe in docs/datasets/Dataset:-{name}.md and applies it.

    Returns
    -------
    dataset : Dataset
        The loaded dataset containing the Polars dataframe and metadata.

    Raises
    ------
    ValueError
        If the dataset name is not found or the source is invalid.
    """
    if source == "uci":
        try:
            uci_data = fetch_ucirepo(id=mixtabank.uci_dict[name]["uci_id"])
        except KeyError:
            raise ValueError(f"Dataset '{name}' not found in the UCI dictionary.")
        # Load dataset from UCI repository into Polars DataFrame
        X = pl.from_pandas(uci_data.data.features)
        Y = pl.from_pandas(uci_data.data.targets)
        df = pl.concat([X, Y], how="horizontal")
        
        target_col_name = mixtabank.uci_dict[name]["target_col"]
        prediction_task = mixtabank.uci_dict[name]["prediction_task"]
        metadata = uci_data.get("metadata")

    elif source == "kaggle":
        try:
            dataset_path = mixtabank.kaggle_dict[name]["kaggle_path"]
            file_name = mixtabank.kaggle_dict[name]["filename"]
        except KeyError:
            raise ValueError(f"Dataset '{name}' not found in the Kaggle dictionary.")
            
        # Load the file directly into a Polars DataFrame
        df = kagglehub.dataset_load(KaggleDatasetAdapter.POLARS, dataset_path, file_name).collect()
        
        target_col_name = mixtabank.kaggle_dict[name]["target_col"]
        prediction_task = mixtabank.kaggle_dict[name]["prediction_task"]
        metadata = None

    else:
        raise ValueError("Source must be either 'uci' or 'kaggle'")

    if curated:
        # Resolve path to docs/datasets/Dataset:-{name}.md
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(mixtabank.__file__)))
        md_path = os.path.join(project_root, "docs", "datasets", f"Dataset:-{name}.md")
        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Find json block under Curated Recipe
                match = re.search(r"## Curated Recipe\s*```json\n(.*?)\n```", content, re.DOTALL)
                if match:
                    try:
                        recipe = json.loads(match.group(1))
                        df = _apply_recipe(df, recipe)
                        if "rename_columns" in recipe and target_col_name in recipe["rename_columns"]:
                            target_col_name = recipe["rename_columns"][target_col_name]
                    except json.JSONDecodeError as e:
                        print(f"Warning: Failed to parse JSON recipe for {name}: {e}")
        else:
            print(f"Warning: Curated option enabled, but {md_path} not found.")

    return Dataset(
        data=df,
        target_col=target_col_name,
        prediction_task=prediction_task,
        metadata=metadata
    )


def download_datasets(names: Union[str, List[str]], output_dir: str, source: str = "uci", curated: bool = False, format: str = "parquet"):
    """
    Mass download datasets and save them to the specified output directory.
    
    Parameters
    ----------
    names : str or list of str
        The dataset name(s) to download. If 'all', downloads all datasets for the given source.
    output_dir : str
        Directory to save the datasets.
    source : str
        'uci' or 'kaggle'
    curated : bool
        If True, applies curated recipes before saving.
    format : str
        Format to save the data ('csv' or 'parquet')
    """
    if isinstance(names, str):
        if names == "all":
            if source == "uci":
                names = list(mixtabank.uci_dict.keys())
            elif source == "kaggle":
                names = list(mixtabank.kaggle_dict.keys())
            else:
                names = []
        else:
            names = [names]
            
    os.makedirs(output_dir, exist_ok=True)
    
    for name in names:
        print(f"Processing dataset: {name}")
        try:
            ds = dataset_loader(name=name, source=source, curated=curated)
            out_path = os.path.join(output_dir, f"{name}.{format}")
            if format == "parquet":
                ds.data.write_parquet(out_path)
            elif format == "csv":
                ds.data.write_csv(out_path)
            print(f"Successfully saved {name} to {out_path}")
        except Exception as e:
            print(f"Failed to process {name}: {e}")
