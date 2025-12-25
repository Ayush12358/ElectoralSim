# Contributing to ElectoralSim

Thank you for your interest in contributing to ElectoralSim!

## Getting Started

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Ayush12358/ElectoralSim.git
cd ElectoralSim

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev,viz]"

# Run tests
pytest tests/ -v
```

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black electoral_sim/

# Lint
ruff check electoral_sim/

# Type check
mypy electoral_sim/
```

## Making Changes

### Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write/update tests
5. Run the test suite: `pytest tests/ -v`
6. Commit with a clear message
7. Push and create a Pull Request

### Commit Messages

Use clear, descriptive commit messages:
- `feat: add new voting system`
- `fix: correct utility calculation in ProximityModel`
- `docs: update API reference`
- `test: add tests for coalition formation`

## Areas for Contribution

### High Priority
- Additional country presets with real party data
- Validation against historical election results
- Performance optimizations

### Medium Priority
- New electoral systems (ranked pairs, star voting)
- Additional opinion dynamics models
- Improved visualization components

### Documentation
- Examples and tutorials
- API documentation improvements
- Translation to other languages

## Testing

All contributions should include tests:

```python
# tests/test_your_feature.py
def test_new_feature():
    from electoral_sim import ElectionModel
    
    model = ElectionModel(n_voters=1000, seed=42)
    result = model.run_election()
    
    assert 'turnout' in result
    assert 0 <= result['turnout'] <= 1
```

## Questions?

Open an issue on GitHub or start a discussion.
