# 🗄️ MixTaBank: A collection of Heterogeneous Mixed-type Tabular Datasets  



> Official codebase for the paper:  
> **"NAME OF PAPER"**  
> [Author1 Name], [Author2 Name], [Institution]  
> 📄 Under review at [Conference/Journal Name], 2025  
> [[Paper PDF]](link-to-paper.com) • [[Website]](optional) • [[Demo Notebook]](notebook-link)

---

## 🔍 Overview

**MixTaBank** is a collection of heterogeneous mixed-type tabular datasets for evaluating tabular generative models under realistic, human-centric conditions. It includes:

- A curated set of real-world, heterogeneous tabular datasets
- Evaluation metrics beyond likelihood, including fidelity, fairness, utility, and structure preservation
- Wrappers for popular generative models: CTGAN, TVAE, TableDiffusion, Gaussian Copula, etc.
- A standardized benchmarking framework and reproducible experiments

---

## 📦 Installation

```bash
git clone https://github.com/your-org/tabgenbench.git
cd tabgenbench
pip install -e .
```

---


## 🧪 Quick Start

```python
from tabgenbench import BenchmarkSuite
from tabgenbench.models import CTGAN
from tabgenbench.metrics import evaluate

# Load benchmark dataset
suite = BenchmarkSuite("credit_default")

# Train generative model
model = CTGAN()
model.fit(suite.train)

# Generate synthetic samples
samples = model.sample(n=1000)

# Evaluate model
results = evaluate(real=suite.test, synthetic=samples)
print(results)
```

---


## 📁 Dataset Guide

| Dataset           | Description                   | Format   |
| ----------------- | ----------------------------- | -------- |
| `credit_default`  | Human-reported financial data | CSV      |
| `churn_modelling` | Customer behavior & attrition | CSV      |
| `coil2000`        | Insurance customer profiles   | ARFF/CSV |
| `adult`           | Classic UCI census dataset    | CSV      |



## 📚 Citation

If you use this library or benchmark in your work, please cite:
```bibtex
@article{your2025tabgenbench,
  title={Grounding Tabular Generative Models in Reality: A Benchmark for Human-Centered Evaluation},
  author={Author1, Firstname and Author2, Firstname},
  journal={Under Review},
  year={2025},
  note={\url{https://github.com/your-org/tabgenbench}}
}
```

## 📄 License

This project is licensed under the MIT License. See LICENSE for details.


## 🔗 Related Projects






