# Electoral Simulation: Stability vs. Proportionality in India

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the source code and research findings for a large-scale (100k agent) Agent-Based Model (ABM) of the Indian electoral system. The project quantifies the trade-off between representational fairness (Gallagher Index) and government stability (Mean Time To Failure) under counterfactual Proportional Representation (PR) rules.

## 🚀 Key Findings (The Grand Audit)
- **The 5% "Stability Bridge"**: Simulations demonstrate that a 5% electoral threshold restores government stability to near-term-limit levels (**4.86 years**) while increasing representational fairness by **88%** (Gallagher 0.06 vs 0.56).
- **The Polarization Trap**: We identify that in highly polarized societies, stability drops to **1.31 years**, highlighting that institutional design provides diminishing returns in fractured social climates.
- **Regional Resilience**: Contrary to common fears, a regional multi-party system remains highly durable under PR (**MTTF 4.05 years**).

## 📊 Visualizations
The model generates high-resolution heatmaps and trade-off frontier charts illustrating the impact of thresholds and societal personas on parliamentary durability.

## 🛠️ Tech Stack
- **Language**: Scala 2.13 (SBT)
- **Visualization**: Python 3 (Seaborn/Matplotlib)
- **Scale**: 100,000 Agents (1:10,000 resolution)

## 🏃 Getting Started
1. **Simulation**: `sbt run`
2. **Visualization**: `python visualize_results.py`
3. **Verification**: `sbt test`

## 📖 Citation
If you use this code or research in your work, please cite:
> Ayush Maurya, (2025). *Simulating the Stability-Proportionality Trade-off: A Computational Counterfactual Analysis of Proportional Representation in the Indian Parliamentary System.*

---
**Author**: Ayush Maurya | **License**: MIT
