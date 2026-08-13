import mixtabank

def main():
    print("Loading census-income_full dataset...")
    dataset = mixtabank.dataset_loader("census-income_full", source="uci", curated=True)
    df = dataset.data
    
    print("\nCardinality of each column:")
    print("-" * 30)
    
    # Calculate cardinality for all columns
    cardinalities = {}
    for col in df.columns:
        cardinalities[col] = df[col].n_unique()
        
    # Sort by cardinality (descending)
    sorted_cardinalities = sorted(cardinalities.items(), key=lambda x: x[1], reverse=True)
    
    for col, card in sorted_cardinalities:
        print(f"{col:20}: {card}")

if __name__ == "__main__":
    main()
