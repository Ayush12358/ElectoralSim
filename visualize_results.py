import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Create reports directory
os.makedirs('reports/figures', exist_ok=True)

# Load Monte Carlo Results
if os.path.exists('data/processed/general_theory_results.csv'):
    df = pd.read_csv('data/processed/general_theory_results.csv')

    # 1. The Dimensionality Curse (MTTF vs Dimensions)
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='dimensions', y='avg_mttf', hue='threshold', data=df, marker='o', palette='viridis')
    plt.title('The Dimensionality Curse: Stability vs Ideological Complexity')
    plt.ylabel('Mean Time To Failure (Years)')
    plt.grid(True)
    plt.savefig('reports/figures/dimensionality_curse.png', dpi=300)
    print("Saved dimensionality_curse.png")

    # 2. The Fragmentation Trap (MTTF vs Party Count) - Faceted by Threshold
    g = sns.FacetGrid(df, col="threshold", col_wrap=2, height=4, aspect=1.5)
    g.map(sns.lineplot, "n_parties", "avg_mttf", "dimensions", palette="tab10", marker="o")
    g.add_legend()
    g.fig.suptitle('Stability Sensitivity to Party Fragmentation', y=1.02)
    plt.savefig('reports/figures/fragmentation_trap.png', dpi=300)
    print("Saved fragmentation_trap.png")

    # 3. The Pareto Efficiency (Gallagher vs MTTF) - Aggregated
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='avg_gallagher', y='avg_mttf', hue='threshold', size='dimensions', sizes=(20, 200), data=df, alpha=0.7, palette='deep')
    plt.title('General Theory Pareto Frontier (All Permutations)')
    plt.xlabel('Disproportionality (Gallagher)')
    plt.ylabel('Stability (MTTF)')
    plt.savefig('reports/figures/general_pareto.png', dpi=300)
    print("Saved general_pareto.png")

else:
    print("Data not found: data/processed/general_theory_results.csv")
