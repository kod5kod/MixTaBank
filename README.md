# 🗄️ MixTaBank: A currated collection of Heterogeneous Mixed-type Tabular Datasets  



<!-- > Official codebase for the paper:  
> **"NAME OF PAPER"**  
> [Author1 Name], [Author2 Name], [Institution]  
> 📄 Under review at [Conference/Journal Name], 2025  
> [[Paper PDF]](link-to-paper.com) • [[Website]](optional) • [[Demo Notebook]](notebook-link) -->

---

## 🔍 Overview

**MixTaBank** is a collection of heterogeneous mixed-type tabular datasets for evaluating tabular generative models under realistic, human-centric conditions. It includes:

- A curated set of real-world, heterogeneous mixed-type tabular datasets
- Datasets with varying degrees of size, complexity, heterogeneity, and cardinality
- Supports loading directly into PANDAS or POLARS dataframes
- Inlcudes data preparation and type conversion utilities
- Easy integration into data pipelines, workflows, and models


---


## 📦 Installation

```bash
git clone https://github.com/kod5kod/MixTaBank.git
cd mixtabank


## CONDA Env:
`conda create -n mixtabank python=3.13`  
`conda activate mixtabank`  
`pip install -r [USER PATH]/requirements.txt`  

## Python's virtualenv:
`virtualenv -p python313 mixtabank `  
`source mixtabank/bin/activate` # for mac/linux  
`.\mixtabank\Scripts\activate` # for windows    
`pip install -r [USER PATH]/requirements.txt`

##  iPython kernel support (optional):
`ipython kernel install --user --name=mixtabank` # adding the kernel to jupyter notebook/lab
```

---


## 🧪 Quick Start

```python
import mixtabank

# Review curreted UCI datasets:
mixtabank.uci_dict

# load a UCI dataset:
df = mixtabank.load_uci("credit_default", source="polars") # or pandas

```

---


<!-- ## 📁 Dataset Guide (old)

| Dataset           | Description                   | Format   | Source   | Link | Prediction Task | Target | # Rows | # Columns | # Cat Features | # Num Features |
| ----------------- | ----------------------------- | -------- | -------- | ---- | --------------- | ------ | ------ | --------- | -------------- | -------------- |
| `churn_modelling` | Customer behavior & attrition | CSV      | Kaggle   | [link](https://www.kaggle.com/uciml/customer-churn-modelling) | Classification | Churn | 7,043 | 20 | 4 | 16 |
| `coil2000`        | Insurance customer profiles   | ARFF/CSV | UCI     | [link](https://archive.ics.uci.edu/ml/datasets/COIL-2000) | Classification | Class | 2,000 | 9 | 2 | 7 |
 -->

## 📁 Dataset Guide

| # | Dataset          | Description                   | Format   | Source   | Link | Prediction Task | Target | # Rows | # Columns | # Num Features  | # Cat Features |  # Total Cardinality |
| -- | ---------------- | ----------------------------- | -------- | -------- | ---- | --------------- | ------ | ------ | --------- | -------------- | -------------- | ----------- | 
| 1 | `taiwanese_bankruptcy` | Taiwanese Bankruptcy Prediction | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction) | Binary Classification | `Bankrupt?` | 6,819 | 95 | 93 | 2 | 4 |
| 2 | `support2` | Critically ill hospitalized patient records    | CSV    | UCI     | [link](https://archive.ics.uci.edu/dataset/880/support2) | Binary Classification | `death` | 9,105 | 45 | 37 | 8 | 38 |
| 3 |`nursery` |  Rank applications for nursery schools | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/76/nursery) | Multiclass Classification | `class` | 12,960 | 9 | 0 | 9 | 32 |
| 4 | `petfinder-tab` | Pet adoption data - tabular only  | CSV    | Kaggle   | [link](https://www.kaggle.com/competitions/petfinder-adoption-prediction/data) | Binary/multiclass Classification | `is_adopted` | 14,993 | 18 | 11 | 7 | 208 |
| 5 | `credit-defualt-taiwan` | Default of Credit Card Clients   | CSV    | UCI     | [link](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) | Binary Classification | `Y` | 30,000 | 24 | 20 | 4 | 15 |
| 6 | `bank-marketing` | Bank marketing data   | CSV    | UCI     | [link](https://archive.ics.uci.edu/dataset/222/bank+marketing) | Binary Classification | `y` | 45,211 | 17 | 7 | 11 | 46 |
| 7 | `adult-census`           | Classic UCI census dataset    | CSV      | UCI     | [link](https://archive.ics.uci.edu/dataset/2/adult) | Binary Classification | `is_high_income` | 48,842 | 15 | 6 | 9 | 107 | 
| 8 | `apartment_rent_classified` | Apartment Rent Classified | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified) | regression | `square_feet`, `price` | 99,826 | 14 | 4 | 10 | 4 |
| 9 | `diabetes_130us` | Diabetes 130-US hospitals for years 1999-2008   | CSV    | UCI     | [link](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008) | Binary Classification | `readmitted` | 101,766  | 48 | 11 | 35 | 2,462 |
| 10 | `home-credit` | Home Credit Default Risk   | CSV    | Kaggle     | [link](https://www.kaggle.com/datasets/datuman/home-credit-default-risk-train-data-tabular/) | Binary Classification | `TARGET` | 210,201  | 17 | 5 | 12 | 121 |
| 11 | `cdc_diabetes` | Diabetes Health Indicators Dataset   | CSV    | UCI     | [link](https://archive.ics.uci.edu/dataset/891/diabetes) | Binary Classification | `Diabetes_binary` | 253,680  | 22 | 7 | 15 | 30 |
| 12 | `mimic-iii` | Critical patients care information  | CSV | Kaggle | [link](https://www.kaggle.com/datasets/datuman/mimic-iii-tabular-limited-features) | Multiclass Classification | `DISCHARGE_LOCATION` | 556,617 | 11 | 3 | 8 | 693 |
| 13 | `covertype` | Forest cover types based on attributes | CSV | UCI | [link](https://archive.ics.uci.edu/dataset/31/covertype) | Multiclass Classification | `Cover_Type` | 581,012 | 55 | 11 | 44 | 93 |













* * *  

## 📚 Citation

If you use this library or benchmark in your work, please cite:
<!-- ```bibtex
@article{your2025mixtabank,
  title={Grounding Tabular Generative Models in Reality: A Benchmark for Human-Centered Evaluation},
  author={Author1, Firstname and Author2, Firstname},
  journal={Under Review},
  year={2025},
  note={\url{https://github.com/kod5kod/MixTaBank}}
}
``` -->

## 📄 License

This project is licensed under the MIT License. See LICENSE for details.


## 🔗 Related Projects


* * *   

  
## Changelog

## 📌 0.02   2025-09-14
* Added UCI datasets walkthrough 
* Added summary table
* Added `get_info` function for datasets
* Data loaded is now source agnostic
* Data loader supports `polars` and `pandas`

## 📌 0.01   2025-09-09
* Initial release
* Added UCI support
* Added UCI datasets


## 📌 0.00   2025-08-01
* Added UCI dict
* Added Kaggle support
* Added README file






