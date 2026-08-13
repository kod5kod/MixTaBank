import mixtabank
import sys

try:
    dataset = mixtabank.dataset_loader("mimic-iii", source="kaggle", curated=False)
    print(dataset.data.columns)
    print(dataset.data.shape)
except Exception as e:
    print(e)
