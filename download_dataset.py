#!/usr/bin/env python3
import argparse
import os
import json
import mixtabank

def main():
    parser = argparse.ArgumentParser(description="Download a dataset from MixTaBank.")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset")
    parser.add_argument("--source", type=str, choices=["uci", "kaggle"], default="uci", help="Source of the dataset (uci or kaggle)")
    parser.add_argument("--output-dir", type=str, required=True, help="Directory to save the dataset")
    parser.add_argument("--format", type=str, choices=["parquet", "csv"], default="parquet", help="Format to save the dataset (default: parquet)")
    parser.add_argument("--df-type", type=str, choices=["polars", "pandas"], default="polars", help="Internal dataframe type for processing (default: polars)")
    parser.add_argument("--no-split", action="store_true", help="Do not split the dataset")
    parser.add_argument("--split", type=float, nargs=3, default=[0.7, 0.15, 0.15], metavar=("TRAIN", "VALID", "TEST"), help="Train, Valid, Test split fractions")
    parser.add_argument("--seed", type=int, default=420, help="Random seed for splitting")
    
    args = parser.parse_args()
    
    print(f"Loading dataset '{args.name}' from {args.source}...")
    try:
        dataset, var_types, target_col_name, prediction_task, metadata = mixtabank.dataset_loader(
            name=args.name, source=args.source, df_type=args.df_type
        )
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    os.makedirs(args.output_dir, exist_ok=True)
    
    splits_sizes = None
    if not args.no_split:
        print(f"Splitting dataset using fractions: {args.split}")
        if args.df_type == "polars":
            train_df, valid_df, test_df = mixtabank.pl_train_valid_test_split(dataset, splits=args.split, seed=args.seed)
            splits_sizes = (train_df.height, valid_df.height, test_df.height)
        else:
            train_df, valid_df, test_df = mixtabank.pd_train_valid_test_split(dataset, splits=args.split, seed=args.seed)
            splits_sizes = (len(train_df), len(valid_df), len(test_df))
            
        for df, split_name in zip([train_df, valid_df, test_df], ["train", "valid", "test"]):
            ext = args.format
            file_path = os.path.join(args.output_dir, f"{args.name}_{split_name}.{ext}")
            print(f"Saving {split_name} set to {file_path}")
            if ext == "parquet":
                if args.df_type == "polars":
                    df.write_parquet(file_path)
                else:
                    df.to_parquet(file_path)
            else:
                if args.df_type == "polars":
                    df.write_csv(file_path)
                else:
                    df.to_csv(file_path, index=False)
                
    else:
        splits_sizes = (len(dataset) if args.df_type == "pandas" else dataset.height, 0, 0)
        ext = args.format
        file_path = os.path.join(args.output_dir, f"{args.name}_full.{ext}")
        print(f"Saving full dataset to {file_path}")
        if ext == "parquet":
            if args.df_type == "polars":
                dataset.write_parquet(file_path)
            else:
                dataset.to_parquet(file_path)
        else:
            if args.df_type == "polars":
                dataset.write_csv(file_path)
            else:
                dataset.to_csv(file_path, index=False)

    print("Generating dataset_info.json...")
    info = mixtabank.generate_dataset_info_json(
        df=dataset, 
        name=args.name, 
        prediction_task=prediction_task, 
        target_col=target_col_name,
        splits_sizes=splits_sizes
    )
    
    info_path = os.path.join(args.output_dir, "dataset_info.json")
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4)
        
    print(f"Finished! All files saved to {args.output_dir}")

if __name__ == "__main__":
    main()
