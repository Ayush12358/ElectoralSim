# ElectoralSim

A configurable, parametric simulation platform for testing electoral system hypotheses.

## Features

- **N-dimensional ideology space**: Model complex, multi-issue political landscapes
- **Multiple electoral systems**: Sainte-Laguë, D'Hondt, thresholds (0-10%)
- **Coalition formation**: Minimum Connected Winning (MCW) strategy
- **Clientelism modeling**: Patronage vs ideology voting
- **Polarization patterns**: Uniform, symmetric, asymmetric voter distributions
- **Stability prediction**: Mean Time To Failure (MTTF) with multiple collapse models
- **Sensitivity analysis**: Minkowski distance metrics, hyperparameter sweeps

## Quick Start

### Prerequisites
- Scala 2.13+
- sbt
- Python 3.x (for visualization)

### Run Simulation
```bash
sbt run
```

### Generate Figures
```bash
pip install -r requirements.txt
python visualize_results.py
```

## Configuration

Edit `CounterfactualMain.scala` to customize:

```scala
val nAgents = 10000                              // Number of voters
val rangeDimensions = Seq(2, 3, 5, 8)            // Issue complexity
val rangeParties = Seq(5, 8, 12, 20)             // Party count
val rangeThresholds = Seq(0.0, 0.05, 0.10)       // Vote threshold
val rangePatronage = Seq(0.0, 0.3, 0.6, 0.9)     // Clientelism level
val polarizationTypes = Seq("Uniform", "Symmetric", "Asymmetric")
val rangeMinkowskiP = Seq(1.0, 2.0, 3.0, 4.0, 5.0)
val collapseModels = Seq("sigmoid", "linear", "exponential")
```

## Project Structure

```
ElectoralSim/
├── src/main/scala/com/simulation/
│   ├── CounterfactualMain.scala   # Monte Carlo runner
│   ├── SimulationEngine.scala     # Core algorithms
│   ├── models/Models.scala        # VoterAgent, Party, Ideology
│   └── utils/ElectoralMath.scala  # Seat allocation, Gallagher Index
├── data/processed/                # Simulation output CSV
├── visualize_results.py           # Figure generation
├── build.sbt                      # Scala build config
└── requirements.txt               # Python dependencies
```

## Output

Results saved to `data/processed/extended_theory_results.csv`:

| Column | Description |
|--------|-------------|
| dimensions | Number of ideological dimensions |
| n_parties | Number of parties |
| threshold | Electoral threshold (0.0 - 0.10) |
| patronage | Clientelism level (0.0 - 0.9) |
| polarization | Voter distribution type |
| minkowski_p | Distance metric parameter |
| collapse_model | MTTF decay model |
| avg_mttf | Mean Time To Failure (years) |
| avg_gallagher | Disproportionality index |
| std_mttf | Standard deviation of MTTF |

## Key Concepts

### Minkowski Distance
- p=1: Manhattan (L1) - sum of absolute differences
- p=2: Euclidean (L2) - standard geometric distance
- p>2: Higher-order - sensitive to large disagreements

### Collapse Models
- **Sigmoid**: Phase transition / tipping point behavior
- **Linear**: Gradual proportional decay
- **Exponential**: Early risk is most damaging

### Coalition Formation (MCW)
Minimum Connected Winning: Start with largest party, add ideologically closest partners until majority reached.

## License

MIT License
