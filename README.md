# Electoral Simulation: Stability vs. Proportionality in India

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the source code and research findings for a large-scale (100k agent) Agent-Based Model (ABM) of the Indian electoral system. The project quantifies the trade-off between representational fairness (Gallagher Index) and government stability (Mean Time To Failure) under counterfactual Proportional Representation (PR) rules across Centrist, Polarized, and Fragmented societal personas.

## 🚀 Key Findings (The Grand Audit)
- **The 5% "Stability Bridge"**: Simulations demonstrate that a 5% electoral threshold restores government stability to near-term-limit levels (~4.8 years) while increasing representational fairness by 75% compared to the FPTP baseline.
- **The Polarization Trap**: We identify that in highly polarized societies, stability drops to **1.31 years**, highlighting that institutional design (thresholds) provides diminishing returns in fractured social climates.
- **Regional Resilience**: Contrary to common "fragmentation fears," a regional multi-party system remains highly durable under PR (MTTF 4.05 years), provided it forms surplus coalitions.

## 🛠️ Tech Stack
- **Language**: Scala 2.13 (SBT)
- **Visualization**: Python 3 (Seaborn/Matplotlib)
- **Scale**: 100,000 Agents (1:10,000 resolution)

## 📂 Project Structure
- `src/main/scala`: Core simulation engine, spatial models, and persona generators.
- `data/processed`: Audited CSV results of the multi-parameter sweep.
- `reports/figures`: Visualization of the Stability-Proportionality Frontier.
- `final_research_paper.md`: The full academic manuscript.

## 🏃 Getting Started
1. **Simulation**: `sbt run` (Generates the audited datasets)
2. **Visualization**: `python visualize_results.py` (Generates heatmaps and frontier charts)
3. **Verification**: `sbt test` (Runs the electoral math unit tests)

## 📖 Citation
If you use this code or research in your work, please cite:
> Ayush Maurya, (2025). *Simulating the Stability-Proportionality Trade-off: A Computational Counterfactual Analysis of Proportional Representation in the Indian Parliamentary System.*

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
