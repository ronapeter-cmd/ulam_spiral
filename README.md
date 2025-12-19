# 🌀 Ulam Spiral Explorer

**Visualizing Prime Numbers with Ulam Spirals**

This project implements tools for generating and exploring the **Ulam spiral** — a classic prime number visualization — along with methods for detecting structured line segments and computing a *goodness* score that quantifies how visually coherent prime patterns are.

---

## 📌 Features

- 🧮 **Ulam Spiral Construction**
  - Fill a square grid with primes arranged in a spiral.
  - Start at different offsets to explore how pattern structure changes.

- 🔎 **Line Segment Detection**
  - Detect and highlight:
    - Main diagonals (↘)
    - Anti-diagonals (↙)
    - Horizontal (→)
    - Vertical (↓)
  - Configurable gap tolerance and minimum run length.

- 📊 **Goodness Metric**
  - Quantifies how “line-like” the prime distribution appears in the spiral.
  - Scores are normalized and comparable across runs.

- 🧰 **Interactive Jupyter UI**
  - Widget UI to explore limit, offset, animation, and detection parameters.
  - Real-time plots and updates within notebooks.

- 📓 **Notebooks Included**
  - Example notebooks demonstrate visualization and analysis.

---

## 📁 Repository Structure

```text
primes/
├── README.md
├── pyproject.toml
├── notebooks/
│   └── Visualize primes.ipynb
└── src/
    └── primes/
        ├── __init__.py
        ├── primes.py              # prime utilities
        ├── ulam_spiral.py         # spiral generation logic
        ├── goodness.py            # run detection & goodness score
        └── viz.py                 # plotting & interactive widgets
🚀 Installation
Prerequisites

Python 3.9+

numpy

matplotlib

ipywidgets

jupyter notebook or lab

Install via pip:

git clone https://github.com/ronapeter-cmd/primes.git
cd primes
pip install -e .

Launch a notebook:

jupyter notebook
📌 Quick Start Examples
🔹 Display an Ulam Spiral

import numpy as np
from primes.ulam_spiral import fill_primes
from primes.viz import display_primes

limit = 100_000
size = int(limit**0.5) + 10
matrix = np.zeros((size, size), dtype=int)

matrix = fill_primes(matrix, offset=1)
display_primes(matrix)
🔹 Detect and Show Diagonals
from primes.goodness import detect_diagonal_segments
from primes.viz import show_with_diagonals

mask = detect_diagonal_segments(matrix, gap_tolerance=2, min_run=20)
show_with_diagonals(matrix, mask)
Blue = primes
Red = detected line segments

🔹 Compute Goodness Score

from primes.goodness import ulam_goodness

score = ulam_goodness(matrix, gap_tolerance=2, min_run=20)
print(f"Goodness score: {score:.4f}")

🔹 Interactive UI
In a notebook cell:

from primes.viz import build_ulam_spiral_ui
build_ulam_spiral_ui()

🔬 About the Goodness Metric
The goodness score measures the fraction of the grid that is covered by run segments (diagonals and HV) that satisfy configured tolerances.
It gives an intuitive sense of how “structured” the prime layout appears visually.

📈 Tips for Exploration
Vary the offset — explore how the spiral structure changes

Tune gap_tolerance and min_run for different behaviors


🧪 Example Notebook
See notebooks/Visualize primes.ipynb for a step-by-step exploration including:

Pattern visualization

Goodness score plots

Offset sweeps - finetune it with the jumps parameter

🛠 Contributing
Contributions are welcome! Consider adding:

Unit tests

Additional UI controls

Alternative detection metrics (e.g., Radon transform or autocorrelation)

Performance improvements

To contribute:

Fork the repository

Create a feature branch

Open a pull request

📄 License
This project is licensed under the MIT License — free to use and modify.

🙏 Acknowledgements
Inspired by Stanislav Ulam’s classic prime spiral visualization and subsequent community explorations of prime structure.
