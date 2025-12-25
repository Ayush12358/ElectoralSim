# Voter Psychology

ElectoralSim models voter psychology using established political science frameworks.

## Big Five Personality (OCEAN)

Each voter has five personality traits that influence their ideology:

| Trait | Range | Political Correlation |
|-------|-------|----------------------|
| **Openness** | 0-1 | Higher → more liberal |
| **Conscientiousness** | 0-1 | Higher → more conservative |
| **Extraversion** | 0-1 | Higher → more politically engaged |
| **Agreeableness** | 0-1 | Higher → more cooperative voting |
| **Neuroticism** | 0-1 | Higher → more responsive to threat appeals |

### Accessing Traits

```python
model = ElectionModel(n_voters=10_000, seed=42)
voter_df = model.voters.df

# View traits
print(voter_df.select([
    "openness", "conscientiousness", "extraversion", 
    "agreeableness", "neuroticism"
]).head())
```

### Research Basis
- High openness correlates with liberal positions (Carney et al., 2008)
- High conscientiousness correlates with conservative positions
- These are implemented as soft influences on ideology generation

---

## Moral Foundations (Haidt)

Five moral foundations that shape political reasoning:

| Foundation | Description | Political Association |
|------------|-------------|----------------------|
| **Care** | Protection from harm | Liberal emphasis |
| **Fairness** | Justice, equality | Liberal emphasis |
| **Loyalty** | In-group solidarity | Conservative emphasis |
| **Authority** | Respect for hierarchy | Conservative emphasis |
| **Sanctity** | Purity, disgust | Conservative emphasis |

### Accessing Foundations

```python
foundations = voter_df.select([
    "mf_care", "mf_fairness", "mf_loyalty", 
    "mf_authority", "mf_sanctity"
])
```

### Research Basis
- Haidt's Moral Foundations Theory (2012)
- Liberals prioritize Care and Fairness
- Conservatives value all five more equally

---

## Affective Polarization

Measures emotional distance between in-group and out-group.

```python
polarization = voter_df["affective_polarization"].to_numpy()
# Range: 0 (no polarization) to 1 (highly polarized)
```

**Effects:**
- High polarization → stronger party loyalty
- High polarization → less responsive to policy changes

---

## Political Knowledge

Voter awareness of political facts and processes.

```python
knowledge = voter_df["political_knowledge"].to_numpy()
# Range: 0-100
```

**Effects:**
- High knowledge → more consistent ideology
- High knowledge → more strategic voting

---

## Misinformation Susceptibility

Vulnerability to false information.

```python
misinfo = voter_df["misinfo_susceptibility"].to_numpy()
# Range: 0-1
```

**Correlates with:**
- Lower political knowledge
- Higher neuroticism
- Lower education

---

## Media Diet

Each voter has a media source preference:

```python
model = ElectionModel(n_voters=10_000, seed=42)

# Media source (0=Left, 1=Center, 2=Right)
media_source = voter_df["media_source_id"]

# Media bias (-0.5=Left, 0=Center, 0.5=Right)
media_bias = voter_df["media_bias"]
```

### Media Sources

| ID | Label | Bias |
|----|-------|------|
| 0 | Left-leaning | -0.5 |
| 1 | Centrist | 0.0 |
| 2 | Right-leaning | +0.5 |

### Selection Mechanism
Voters are more likely to consume media aligned with their ideology (selective exposure).

---

## Economic Perception

Sociotropic vs Pocketbook voting distinction:

```python
perception = voter_df["economic_perception"].to_numpy()
# 0 = Pocketbook (personal finances)
# 1 = Sociotropic (national economy)
```

**Research:**
- Higher education → more sociotropic
- Used by `SociotropicPocketbookModel`
