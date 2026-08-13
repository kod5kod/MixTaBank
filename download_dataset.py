#!/usr/bin/env python3
import argparse
import os
import json
import mixtabank

def main():
    parser = argparse.ArgumentParser(description="Download a dataset from MixTaBank.")
    parser.add_argument("--names", type=str, nargs="+", help="Name(s) of the dataset(s) to download")
    parser.add_argument("--all", action="store_true", help="Download all available datasets for the source")
    parser.add_argument("--source", type=str, choices=["uci", "kaggle", "all"], default="all", help="Source of the dataset (uci or kaggle) when using --all. Ignored when passing --names.")
    parser.add_argument("--output-dir", type=str, required=True, help="Directory to save the dataset")
    parser.add_argument("--format", type=str, choices=["parquet", "csv"], default="parquet", help="Format to save the dataset (default: parquet)")
    parser.add_argument("--curated", action="store_true", help="Apply curated preprocessing recipes if available")
    parser.add_argument("--no-split", action="store_true", help="Do not split the dataset")
    parser.add_argument("--split", type=float, nargs=3, default=[0.7, 0.15, 0.15], metavar=("TRAIN", "VALID", "TEST"), help="Train, Valid, Test split fractions")
    parser.add_argument("--seed", type=int, default=420, help="Random seed for splitting")
    
    args = parser.parse_args()
    
    if not args.names and not args.all:
        print("Error: Must specify either --names or --all")
        return
        
    os.makedirs(args.output_dir, exist_ok=True)
    
    datasets_to_process = []
    
    if args.all:
        if args.source in ["uci", "all"]:
            datasets_to_process.extend([(name, "uci") for name in mixtabank.uci_dict.keys()])
        if args.source in ["kaggle", "all"]:
            datasets_to_process.extend([(name, "kaggle") for name in mixtabank.kaggle_dict.keys()])
    else:
        aliases = {
            "credit-default-taiwan": "credit_default_taiwan",
            "credit-defualt-taiwan": "credit_default_taiwan",
            "beijing": "beijing_pm25",
            "bank-marketing": "bank_marketing",
            "adult-census": "adult_census",
            "census-income_full": "census_income_full",
            "petfinder-tab": "petfinder_tab",
            "home-credit": "home_credit",
            "mimic-iii": "mimic_iii",
            "criteo-1m": "criteo_1m"
        }
        for raw_name in args.names:
            name = aliases.get(raw_name, raw_name)
            
            if name in mixtabank.uci_dict:
                datasets_to_process.append((name, "uci"))
            elif name in mixtabank.kaggle_dict:
                datasets_to_process.append((name, "kaggle"))
            else:
                datasets_to_process.append((name, None))
                
    successes = []
    failures = []
        
    for name, source in datasets_to_process:
        if source is None:
            # Helpful hints for common typos
            hints = ""
            if "default" in name: hints = " (Did you mean 'credit-defualt-taiwan'?)"
            if "beijing" == name: hints = " (Did you mean 'beijing_pm25'?)"
            
            msg = f"Dataset '{name}' not found in either UCI or Kaggle dictionaries.{hints}"
            print(f"Error: {msg}")
            failures.append((name, msg))
            continue
            
        print(f"Loading dataset '{name}' from {source}...")
        try:
            ds = mixtabank.dataset_loader(
                name=name, source=source, curated=args.curated
            )
        except Exception as e:
            msg = f"Error loading dataset {name}: {e}"
            print(msg)
            failures.append((name, msg))
            continue
            
        dataset_out_dir = os.path.join(args.output_dir, name)
        os.makedirs(dataset_out_dir, exist_ok=True)
            
        splits_sizes = None
        if not args.no_split:
            print(f"Splitting dataset {name} using fractions: {args.split}")
            train_df, valid_df, test_df = mixtabank.train_valid_test_split(ds.data, splits=args.split, seed=args.seed)
            splits_sizes = (train_df.height, valid_df.height, test_df.height)
            
            for df, split_name in zip([train_df, valid_df, test_df], ["train", "valid", "test"]):
                ext = args.format
                file_path = os.path.join(dataset_out_dir, f"{split_name}.{ext}")
                print(f"Saving {split_name} set to {file_path}")
                if ext == "parquet":
                    df.write_parquet(file_path)
                else:
                    df.write_csv(file_path)
        else:
            splits_sizes = (ds.data.height, 0, 0)
            ext = args.format
            file_path = os.path.join(dataset_out_dir, f"full.{ext}")
            print(f"Saving full dataset to {file_path}")
            if ext == "parquet":
                ds.data.write_parquet(file_path)
            else:
                ds.data.write_csv(file_path)

        print(f"Generating info.json for {name}...")
        info = mixtabank.generate_dataset_info_json(
            df=ds.data, 
            name=name, 
            prediction_task=ds.prediction_task, 
            target_col=ds.target_col,
            splits_sizes=splits_sizes
        )
        
        info_path = os.path.join(dataset_out_dir, "info.json")
        with open(info_path, "w", encoding="utf-8") as f:
            json.dump(info, f, indent=4)
            
        successes.append(name)
            
    print("\n" + "="*50)
    print("DOWNLOAD REPORT")
    print("="*50)
    print(f"Successful ({len(successes)}):")
    for s in successes:
        print(f"  - {s}")
    
    if failures:
        print(f"\nFailed ({len(failures)}):")
        for f, msg in failures:
            print(f"  - {f}: {msg}")
    print("="*50)

if __name__ == "__main__":
    main()
