---
marp: true
theme: gaia
class: lead
backgroundColor: #0e1117
color: #e6edf3
style: |
  section {
    font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 28px;
    background-image: linear-gradient(135deg, #0e1117 0%, #161b22 100%);
  }
  h1 {
    color: #ff4b4b;
    font-size: 70px;
    font-weight: 800;
    margin-bottom: 20px;
  }
  h2 {
    color: #58a6ff;
    font-weight: 600;
  }
  h3 {
    color: #d2a8ff;
    margin-top: 10px;
  }
  strong {
    color: #7ee787;
  }
  a {
    color: #79c0ff;
    text-decoration: none;
  }
  code {
    background-color: #1f2428;
    color: #ff7b72;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
  }
  blockquote {
    background: #1f2428;
    border-left: 10px solid #ff4b4b;
    margin: 1.5em 10px;
    padding: 0.5em 10px;
    color: #c9d1d9;
  }
  ul {
    list-style-type: none;
    padding-left: 0;
  }
  li {
    margin-bottom: 12px;
    padding-left: 20px;
    position: relative;
  }
  li::before {
    content: "\2022";
    color: #ff4b4b;
    font-weight: bold;
    display: inline-block; 
    width: 1em;
    margin-left: -1em;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

# ElectoralSim
## Advanced Agent-Based Electoral Simulation Toolkit

**A High-Performance Computational Framework for Analyzing Democracy**

Ayush | 2026

---

<!-- _class: default -->

## 1. The Problem: Why Simulation Matters?

**Real-world experiments on electoral systems are impossible.**

<div class="columns">
<div>

- You cannot "A/B Test" a country's democracy.
- Policy makers often guess the impact of changes.
- Existing tools are often "toy models" or purely statistical, lacking individual agency.

</div>
<div>

> **We need a sandbox to test the resilience and fairness of democratic systems.**

</div>
</div>

---

<!-- _class: default -->

## 2. The Solution: ElectoralSim

**ElectoralSim** is a large-scale Agent-Based Model (ABM) that simulates elections from the bottom up.

<div class="columns">
<div>

### Micro-Level
Simulates **millions of individual voters** with unique personalities, biases, and media diets.

</div>
<div>

### Macro-Level
Emergent political dynamics, coalition formation, and systemic stability.

</div>
</div>

*Bridges the gap between Political Science theory and Computational scale.*

---

## 3. Technology Stack (The "Secret Sauce")

How do we simulate **1 Million+ Agents** in near real-time?

### 1. Polars DataFrames
Replaces standard Python objects with columnar, SIMD-optimized data structures.

### 2. Numba & JIT
Compiles critical simulation loops to machine code (approaching C++ speeds).

### 3. Modern ABM
Built on `Mesa`, but supercharged for vectorized operations.

### 4. Interactive Frontend
`Streamlit` + `Plotly` for real-time visualization and exploration.

---

<!-- _class: default -->

## 4. Key Features

<div class="columns">
<div>

### Complex Voter Behavior
- **Spatial Voting**: Voters choose parties closest to their ideology.
- **Strategic Voting**: "I want Party A, but they won't win, so I vote Party B."
- **Economic Voting**: Punishing incumbents for poor economic performance.

</div>
<div>

### Real-World Presets
- **India (Lok Sabha)**: 543 Constituencies, First-Past-The-Post.
- **Germany (Bundestag)**: Mixed-Member Proportional (MMP).
- **USA, UK, France, Brazil**: Pre-configured with real party data.

</div>
</div>

---

## 5. Advanced Metrics & Analytics

We don't just count votes; we measure **democratic health**.

- **Gallagher Index**: Mathematically measures how "unfair" an election result is (Disproportionality).
- **Swing Analysis**: "What if the ruling party lost 5% vote share?" - visualize the seat flip instantly.
- **Effective Number of Parties (ENP)**: Measures political fragmentation.
- **Voter Satisfaction Efficiency (VSE)**: How well the outcome represents the median voter.

---

<!-- class: lead -->

# Live Demo

**Scale. Speed. Fairness.**

_Simulating India's 2024 Election in < 200 ms_
