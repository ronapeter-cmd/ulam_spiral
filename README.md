📐 Ulam Spiral Explorer

Prime visualization, diagonal pattern detection, goodness scoring, and interactive exploration tools

This project implements an extensible and modular framework for studying the visual structure of prime numbers using the Ulam spiral and related techniques.

It includes:

Efficient prime–spiral generation

Diagonal, horizontal, and vertical structure detection

A “goodness” metric that quantifies the visual coherence of prime lines

An interactive Jupyter UI for exploring offsets, parameters, and patterns

Notebook examples for experimentation

(Experimental) ideas for 3D extensions of Ulam’s concept

🚀 Features
🌀 Ulam Spiral Construction

Generate large 2D Ulam spirals with an adjustable starting offset.

🔍 Line Structure Detection

Detect visually coherent:

Main diagonal segments (↘)

Anti-diagonal segments (↙)

Horizontal segments (→)

Vertical segments (↓)

with configurable gap tolerance and minimum run length.

📊 Goodness Metric

A scalar score describing “how line-like” an Ulam matrix is.

Higher values indicate stronger global diagonal structure.

🎛 Interactive UI (Jupyter)

Explore Ulam spirals with widgets:

Select prime limit

Adjust offset

Show/hide diagonal detection

Run animations (varying offsets)

Tune gap tolerance & minimum run parameters

📓 Example Notebooks

Includes a step-by-step exploration notebook showing:

How primes arrange into diagonal patterns

How the goodness score varies with offset

How detection parameters affect the segmentation

📦 Project Structure
primes/
├── README.md
├── pyproject.toml
├── notebooks/
│   └── Visualize primes.ipynb
└── src/
    └── primes/
        ├── __init__.py
        ├── primes.py              # prime utilities (is_prime etc.)
        ├── ulam_spiral.py         # fill_primes + Ulam matrix construction
        ├── goodness.py            # diagonal + HV detection + goodness metric
        └── viz.py                 # plotting + interactive UI

🔧 Installation

This project uses numpy, matplotlib, and ipywidgets.

Clone and install in development mode:

git clone https://github.com/<your-username>/primes.git
cd primes
pip install -e .


Launch Jupyter:

jupyter notebook

🧠 Quick Start
1. Generate and display an Ulam spiral
import numpy as np
from primes.ulam_spiral import fill_primes
from primes.viz import display_primes

limit = 100000
size = int(limit**0.5) + 10
matrix = np.zeros((size, size), dtype=int)

matrix = fill_primes(matrix, offset=1)
display_primes(matrix)

2. Detect and visualize diagonal segments
from primes.goodness import detect_diagonal_segments
from primes.viz import show_with_diagonals

mask = detect_diagonal_segments(matrix, gap_tolerance=2, min_run=20)
show_with_diagonals(matrix, mask)


Blue → all primes
Red → detected line segments

3. Compute the global “goodness” score
from primes.goodness import ulam_goodness

score = ulam_goodness(matrix, gap_tolerance=2, min_run=20)
print("Goodness:", score)

4. Explore with the interactive UI
from primes.viz import build_ulam_spiral_ui
build_ulam_spiral_ui()


This opens:

Limit selector

Offset selector

Toggle: show diagonals

Animation over offsets

Tuning of gap tolerance & min run

Live updates inside the notebook

5. Scan offsets and find the best one
scores = []
offsets = range(0, 1000)

for off in offsets:
    m = fill_primes(np.zeros((size,size), int), offset=off)
    s = ulam_goodness(m, gap_tolerance=2, min_run=20)
    scores.append(s)

best_offset = offsets[np.argmax(scores)]
print("Best offset:", best_offset)

🧪 Research Notes

Ulam spirals exhibit surprisingly strong diagonal structure.
This project provides tools to quantify and visualize these effects:

Prime distributions create polynomial-diagonals

The goodness metric correlates with “visual order”

Offsets significantly change the structure

Gap tolerance controls how “broken” diagonal patterns are interpreted


🛠 Future Work

Add 3D visualization (plot Ulam shells on a 3D lattice)

GPU-accelerated prime filling for very large grids

Better statistical evaluation of goodness scores

Radon-transform-based line detection

Heatmaps for local diagonal density

📄 License

MIT License — free to use and modify.

🙏 Acknowledgements

Inspired by Stanislaw Ulam’s original observation (1963), and by subsequent mathematical and computational studies on prime spatial structure
