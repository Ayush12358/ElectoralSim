import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Ensure figures directory exists
os.makedirs('figures', exist_ok=True)

# Load Extended Theory Results
if os.path.exists('data/processed/extended_theory_results.csv'):
    df = pd.read_csv('data/processed/extended_theory_results.csv')
    
    # 1. Clientelism Effect: MTTF vs Patronage Level
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='patronage', y='avg_mttf', hue='threshold', style='polarization', 
                 data=df[df['dimensions']==5], marker='o', palette='viridis')
    plt.title('Clientelism Effect: Stability vs Patronage Weight (5D)')
    plt.xlabel('Patronage Affinity (0=Ideology, 1=Patronage)')
    plt.ylabel('Mean Time To Failure (Years)')
    plt.grid(True)
    plt.savefig('figures/clientelism_effect.png', dpi=300)
    print("Saved clientelism_effect.png")

    # 2. Asymmetric Polarization Comparison
    plt.figure(figsize=(12, 5))
    df_5d = df[(df['dimensions']==5) & (df['threshold']==0.05) & (df['patronage']==0.0)]
    sns.barplot(x='polarization', y='avg_mttf', data=df_5d, palette='Set2')
    plt.title('Asymmetric Polarization Effect (5D, 5% Threshold)')
    plt.ylabel('Mean Time To Failure (Years)')
    plt.xlabel('Polarization Type')
    plt.savefig('figures/asymmetric_polarization.png', dpi=300)
    print("Saved asymmetric_polarization.png")

    # 3. Combined Heatmap: Patronage x Polarization
    plt.figure(figsize=(10, 8))
    df_pivot = df[(df['dimensions']==5) & (df['threshold']==0.05)].pivot_table(
        values='avg_mttf', index='patronage', columns='polarization', aggfunc='mean'
    )
    sns.heatmap(df_pivot, annot=True, cmap='RdYlGn', fmt=".2f")
    plt.title('Stability: Patronage x Polarization (5D, 5% Threshold)')
    plt.xlabel('Polarization Type')
    plt.ylabel('Patronage Affinity')
    plt.savefig('figures/patronage_polarization_heatmap.png', dpi=300)
    print("Saved patronage_polarization_heatmap.png")

    # 4. Pareto Frontier (Updated)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='avg_gallagher', y='avg_mttf', hue='polarization', 
                    size='patronage', sizes=(20, 200), data=df, alpha=0.7, palette='deep')
    plt.title('Extended Pareto Frontier: Fairness vs Stability')
    plt.xlabel('Disproportionality (Gallagher)')
    plt.ylabel('Stability (MTTF)')
    plt.savefig('figures/extended_pareto.png', dpi=300)
    print("Saved extended_pareto.png")

else:
    print("Data not found: data/processed/extended_theory_results.csv")
    # Fall back to general theory results
    if os.path.exists('data/processed/general_theory_results.csv'):
        df = pd.read_csv('data/processed/general_theory_results.csv')
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='dimensions', y='avg_mttf', hue='threshold', data=df, marker='o', palette='viridis')
        plt.title('The Dimensionality Curse: Stability vs Ideological Complexity')
        plt.ylabel('Mean Time To Failure (Years)')
        plt.grid(True)
        plt.savefig('figures/dimensionality_curse.png', dpi=300)
        print("Saved dimensionality_curse.png")
