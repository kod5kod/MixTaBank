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
| `credit_default`  | Human-reported financial data | CSV      | Kaggle   | [link](https://www.kaggle.com/uciml/default-of-credit-card-clients-dataset) | Classification | default | 30,000 | 25 | 6 | 19 | 
| `churn_modelling` | Customer behavior & attrition | CSV      | Kaggle   | [link](https://www.kaggle.com/uciml/customer-churn-modelling) | Classification | Churn | 7,043 | 20 | 4 | 16 |
| `coil2000`        | Insurance customer profiles   | ARFF/CSV | UCI     | [link](https://archive.ics.uci.edu/ml/datasets/COIL-2000) | Classification | Class | 2,000 | 9 | 2 | 7 |
| `adult`           | Classic UCI census dataset    | CSV      | UCI     | [link](https://archive.ics.uci.edu/ml/datasets/Adult) | Classification | Income | 32,561 | 14 | 6 | 8 |
| `census`          | Classic UCI census dataset    | CSV      | UCI     | [link](https://archive.ics.uci.edu/ml/datasets/Census) | Classification | Income | 32,561 | 14 | 6 | 8 | -->

## 📁 Dataset Guide

| Dataset          | Description                   | Format   | Source   | Link | Prediction Task | Target | # Rows | # Columns | # Num Features  | # Cat Features |  # Total Cardinality |
| ----------------- | ----------------------------- | -------- | -------- | ---- | --------------- | ------ | ------ | --------- | -------------- | -------------- | ------------- |
| `petfinder-tab` | Pet adoption data - tabular only  | CSV    | Kaggle   | [link](https://www.kaggle.com/competitions/petfinder-adoption-prediction/data) | Binary/multiclass Classification | `is_adopted` | 14,993 | 18 | 11 | 7 | 208 |
| `bank-marketing` | Bank marketing data   | CSV    | UCI     | [link](https://archive.ics.uci.edu/dataset/222/bank+marketing) | Binary Classification | `y` | 45,211 | 17 | 7 | 10 | 46 |
| `adult-census`           | Classic UCI census dataset    | CSV      | UCI     | [link](https://archive.ics.uci.edu/dataset/2/adult) | Binary Classification | `is_high_income` | 48,842 | 14 | 6 | 9 | 107 | 


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

## 📌 0.01   2025-09-09
* Initial release
* Added UCI support
* Added UCI datasets


## 📌 0.00   2025-08-01
* Added UCI dict
* Added Kaggle support
* Added README file






