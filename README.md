# Towards a General Theory of Electoral Stability

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Monte Carlo simulation framework for studying the relationship between electoral system design, political complexity, and government stability. This research identifies **five structural principles** governing democratic stability across N-dimensional political landscapes.

---

## 📊 Key Findings

| Principle | Finding |
|-----------|---------|
| **I. Dimensionality Constraint** | Stability decays exponentially as ideological complexity (D) increases |
| **II. Fragmentation Trade-off** | Beyond 8 parties, MTTF drops below 3 years in pure PR systems |
| **III. 5% Threshold Effect** | A 5% threshold universally restores stability to >4 years |
| **IV. Clientelism Effect** | High patronage (0.9) creates stability immune to fragmentation |
| **V. Asymmetric Polarization** | One-sided dominance creates more stable governments than symmetric competition |

---

## � Repository Structure

```
electoral-simulation/
├── main.tex                 # Research paper (LaTeX)
├── references.bib           # Bibliography (21 citations, APA style)
│
├── src/                     # Scala simulation code
│   └── main/scala/com/simulation/
│       ├── CounterfactualMain.scala   # Monte Carlo runner
│       ├── SimulationEngine.scala     # Core logic (MTTF, vote scoring)
│       ├── models/Models.scala        # VoterAgent, Party, Ideology
│       └── utils/
│           └── ElectoralMath.scala    # Gallagher Index, seat allocation
│
├── visualize_results.py     # Python script for generating figures
│
├── data/processed/
│   ├── extended_theory_results.csv    # Full results (17,280 rows)
│   └── general_theory_results.csv     # Base theory results
│
├── figures/                 # Generated plots (used in paper)
│   ├── dimensionality_curse.png       # Principle I
│   ├── fragmentation_trap.png         # Principle II
│   ├── general_pareto.png             # Principle III
│   ├── clientelism_effect.png         # Principle IV
│   ├── asymmetric_polarization.png    # Principle V
│   └── patronage_polarization_heatmap.png
│
├── build.sbt                # Scala build configuration
├── project/build.properties
├── requirements.txt         # Python dependencies
└── LICENSE
```

---

## 🚀 Reproducing Results

### Prerequisites
- **Scala**: 2.13.x with SBT
- **Python**: 3.8+ with pandas, matplotlib, seaborn, numpy

### Step 1: Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt
```

### Step 2: Run the Simulation

```bash
# Run Monte Carlo simulation (generates CSV in data/processed/)
sbt run
```

**Parameters swept:**
- Dimensions: {2, 3, 4, 5, 8}
- Parties: {3, 5, 8, 12, 16, 20}
- Thresholds: {0%, 3%, 5%, 10%}
- Patronage: {0.0, 0.3, 0.6, 0.9}
- Polarization: {Uniform, Symmetric, Asymmetric}

**Output:** `data/processed/extended_theory_results.csv`

### Step 3: Generate Figures

```bash
# Generate all plots for the paper
python visualize_results.py
```

**Output:** PNG files in `figures/`

### Step 4: Compile the Paper

```bash
# Compile LaTeX (requires pdflatex and bibtex)
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

**Output:** `main.pdf`

---

## 🔧 Code Overview

### Core Simulation (`SimulationEngine.scala`)
- `calculateDistance()` - N-dimensional Euclidean distance
- `calculateVoteScore()` - Blends ideology and patronage: `Score = (1-α)·ideology + α·patronage`
- `calculateMTTF()` - Sigmoid stability function based on coalition strain
- `generateClusteredIdeology()` - Creates polarization distributions

### Monte Carlo Runner (`CounterfactualMain.scala`)
- Sweeps across all parameter combinations
- Generates voters based on polarization type
- Forms minimum winning coalitions
- Records Gallagher Index and MTTF per trial

### Electoral Math (`ElectoralMath.scala`)
- `gallagherIndex()` - Measures vote-seat disproportionality
- `allocateSainteLague()` - Proportional seat allocation

---

## 📖 Citation

If you use this code or research, please cite:

```bibtex
@article{Maurya2025,
  author  = {Ayush Maurya},
  title   = {Towards a General Theory of Electoral Stability: 
             A Monte Carlo Analysis of High-Dimensional Political Landscapes},
  year    = {2025},
  institution = {IIIT Hyderabad}
}
```

---

## 🤖 AI Disclosure

This project was developed using **Google Antigravity**. All logical rules, parameters, and outputs were manually verified by the author.

---

**Author:** Ayush Maurya | **Institution:** IIIT Hyderabad | **License:** MIT
