# Installation

## Requirements

- Python 3.11 or higher
- pip (Python package manager)

## Basic Installation

```bash
# Clone the repository
git clone https://github.com/Ayush12358/ElectoralSim.git
cd ElectoralSim

# Install in editable mode
pip install -e .
```

## Optional Dependencies

### Visualization
For charts, plots, and the Streamlit dashboard:
```bash
pip install -e ".[viz]"
```
This installs: `matplotlib`, `plotly`, `streamlit`

### GPU Acceleration
For CUDA-accelerated simulations with large voter populations:
```bash
pip install -e ".[gpu]"
```
This installs: `cupy`

> **Note:** GPU support requires NVIDIA CUDA toolkit. See [CuPy installation guide](https://docs.cupy.dev/en/stable/install.html).

### Development
For running tests and contributing:
```bash
pip install -e ".[dev]"
```
This installs: `pytest`, `pytest-cov`

### All Dependencies
```bash
pip install -e ".[dev,viz,gpu]"
```

## Verification

Test your installation:
```python
from electoral_sim import ElectionModel

model = ElectionModel(n_voters=1000, seed=42)
results = model.run_election()
print(f"Installation successful! Turnout: {results['turnout']:.1%}")
```

## Troubleshooting

### ImportError: No module named 'mesa'
```bash
pip install mesa>=3.0.0
```

### Numba warnings
Numba JIT compilation warnings on first run are normal. They disappear after the first execution.

### GPU not detected
Ensure CUDA is installed and `cupy` can access your GPU:
```python
import cupy as cp
print(cp.cuda.runtime.getDeviceCount())  # Should return >= 1
```
