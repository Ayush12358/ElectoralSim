import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create reports directory if it doesn't exist
os.makedirs('reports/figures', exist_ok=True)

# Load the extended results
df = pd.read_csv('data/processed/extended_simulation_results.csv')

# 1. Trade-off Plot (Gallagher vs MTTF) for a standard shock (0.2)
plt.figure(figsize=(12, 7))
sns.set_style("whitegrid")
df_std = df[df['shock_magnitude'] == 0.2]

fig, ax1 = plt.subplots(figsize=(12, 7))

color = 'tab:red'
ax1.set_xlabel('Electoral Threshold')
ax1.set_ylabel('Gallagher Index (Disproportionality)', color=color)
ax1.plot(df_std['threshold'], df_std['gallagher_index'], color=color, marker='o', linewidth=2, label='Gallagher Index')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('MTTF (Stability Years)', color=color)
ax2.plot(df_std['threshold'], df_std['mttf'], color=color, marker='s', linestyle='--', linewidth=2, label='MTTF')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('The Stability-Proportionality Frontier (Extended Range)', fontsize=14)
fig.tight_layout()
plt.savefig('reports/figures/tradeoff_frontier_extended.png', dpi=300)
print("Extended chart saved to reports/figures/tradeoff_frontier_extended.png")

# 2. Heatmap: Stability across Thresholds and Shock Magnitudes
plt.figure(figsize=(10, 8))
pivot_df = df.pivot(index='threshold', columns='shock_magnitude', values='mttf')
sns.heatmap(pivot_df, annot=True, cmap='RdYlGn', fmt=".2f")
plt.title('Stability (MTTF) across Thresholds & Shock Scenarios')
plt.savefig('reports/figures/stability_heatmap.png', dpi=300)
print("Heatmap saved to reports/figures/stability_heatmap.png")
