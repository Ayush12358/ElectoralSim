# Country Presets

Detailed documentation for all country presets.

## USA

Two-party system with 435 House districts.

```python
model = ElectionModel.from_preset("usa", n_voters=100_000)
```

| Party | Position | Description |
|-------|----------|-------------|
| Democrats | Left | Center-left coalition |
| Republicans | Right | Conservative coalition |

---

## UK

First-past-the-post with 650 Commons seats.

```python
model = ElectionModel.from_preset("uk", n_voters=100_000)
```

| Party | Position |
|-------|----------|
| Conservative | Right |
| Labour | Left |
| Liberal Democrats | Center |
| SNP | Center-Left (Scotland) |
| Plaid Cymru | Left (Wales) |
| Green | Left |

---

## Germany

Mixed-member proportional (MMP) with 5% threshold.

```python
model = ElectionModel.from_preset("germany", n_voters=100_000)
```

| Party | Position |
|-------|----------|
| CDU/CSU | Center-Right |
| SPD | Center-Left |
| Grüne | Left |
| FDP | Liberal |
| AfD | Right |
| Linke | Left |

**System:** PR with Sainte-Laguë allocation and 5% threshold

---

## France

Two-round legislative elections.

```python
from electoral_sim import france_config

config = france_config(n_voters=100_000)
```

| Party | Position |
|-------|----------|
| Renaissance | Center |
| RN | Right |
| LFI | Left |
| LR | Center-Right |
| PS | Center-Left |
| EELV | Left-Green |
| PCF | Left |

---

## Brazil

Largest PR system with 513 deputies.

```python
from electoral_sim import brazil_config
```

**System:** Open-list PR with D'Hondt allocation

---

## Japan

Mixed-member parallel system.

```python
from electoral_sim import japan_config
```

| Party | Position |
|-------|----------|
| LDP | Center-Right |
| CDP | Center-Left |
| Komeito | Center |
| JCP | Left |
| Ishin | Right |
| DPP | Center |

**System:** FPTP (289 seats) + PR (176 seats)

---

## Australia

### House of Representatives (IRV)

```python
from electoral_sim import australia_house_config
```

**System:** Instant Runoff Voting (151 seats)

### Senate (STV)

```python
from electoral_sim import australia_senate_config
```

**System:** Single Transferable Vote (76 seats)

| Party | Position |
|-------|----------|
| Liberal/National | Right |
| Labor | Left |
| Greens | Left |
| One Nation | Right |
| Independent | Various |

---

## South Africa

Pure PR with no threshold.

```python
from electoral_sim import south_africa_config
```

| Party | Position |
|-------|----------|
| ANC | Center-Left |
| DA | Center-Right |
| EFF | Left |
| IFP | Center |
| FF+ | Right |
| MK | Left |

**System:** PR with D'Hondt (400 National Assembly seats)

---

## EU Parliament

27 member states, 720 MEPs, 8 political groups.

```python
from electoral_sim import simulate_eu_election, EU_MEMBER_STATES

result = simulate_eu_election(
    n_voters_per_mep=500,
    seed=42,
    verbose=True
)

print(f"Total seats: {sum(result.seats.values())}")
print(f"Pro-EU seats: {result.pro_eu_seats}")
print(f"Eurosceptic seats: {result.eurosceptic_seats}")
```

### Political Groups

| Group | Position | Description |
|-------|----------|-------------|
| EPP | Center-Right | European People's Party |
| S&D | Center-Left | Socialists & Democrats |
| Renew | Liberal | Renew Europe |
| Greens/EFA | Left-Green | Greens/Free Alliance |
| ECR | Right | Conservatives & Reformists |
| ID | Right | Identity & Democracy |
| The Left | Left | GUE/NGL |
| NI | Various | Non-Inscrits |

### Member States

All 27 EU members are simulated with proportional seat allocation based on population:

- Germany (96), France (81), Italy (76), Spain (61)
- Poland (52), Romania (33), Netherlands (31)
- And 20 more...

### Result Structure

```python
class EUElectionResult:
    seats: dict[str, int]           # Group -> seats
    country_results: dict           # Country-wise breakdown
    pro_eu_seats: int               # Pro-integration groups
    eurosceptic_seats: int          # Eurosceptic groups
    turnout: float                  # Average turnout
```
