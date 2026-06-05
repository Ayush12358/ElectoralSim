# Constituency Management

Constituency metadata structures and management for real-world electoral district data including names, states, types (reserved/general), candidate eligibility, and voter demographics.

---

## ConstituencyMetadata

Dataclass holding metadata for a single electoral district.

```python
from electoral_sim.core.constituency import ConstituencyMetadata

const = ConstituencyMetadata(
    id=1,
    name="Mumbai South",
    state="Maharashtra",
    seats=1,
    type="General",
    lat=18.9750,
    lon=72.8258,
)
```

**Fields:**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | int | *required* | Unique constituency identifier |
| `name` | str | *required* | Constituency name |
| `state` | str | *required* | State or province name |
| `seats` | int | `1` | Number of seats in this constituency |
| `type` | str | `"General"` | Constituency type (e.g., `"General"`, `"SC"`, `"ST"`) |
| `metadata` | `dict[str, Any]` | `{}` | Arbitrary additional metadata |
| `lat` | `float \| None` | `None` | Latitude coordinate |
| `lon` | `float \| None` | `None` | Longitude coordinate |

---

## ConstituencyManager

Manages a collection of constituencies for a simulation, backed by a Polars DataFrame.

```python
from electoral_sim.core.constituency import ConstituencyManager, ConstituencyMetadata

# From a list of ConstituencyMetadata
constits = [
    ConstituencyMetadata(0, "North", "State A"),
    ConstituencyMetadata(1, "South", "State A"),
]
manager = ConstituencyManager(constits)

# From a Polars DataFrame
import polars as pl
df = pl.DataFrame({"id": [0, 1], "name": ["North", "South"], "state": ["A", "A"]})
manager = ConstituencyManager(df)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `constituencies` | `list[ConstituencyMetadata] \| pl.DataFrame` | Constituency data |

### get_name

```python
def get_name(self, const_id: int) -> str
```

Return constituency name for a given ID. Returns `"District {id}"` if not found.

### get_state

```python
def get_state(self, const_id: int) -> str
```

Return state/province name for a constituency ID. Returns `"Unknown"` if not found.

### get_type

```python
def get_type(self, const_id: int) -> str
```

Return constituency type (`"General"`, `"SC"`, `"ST"`) for a constituency ID. Returns `"General"` if not found or type column missing.

### to_dict_list

```python
def to_dict_list(self) -> list[dict]
```

Export all constituencies as a list of dicts.

**Example:**
```python
manager = ConstituencyManager(constituencies_list)
names = [c["name"] for c in manager.to_dict_list()]
```

---

## is_candidate_eligible

Check if a candidate is eligible to contest in a constituency of a given type.

```python
from electoral_sim.core.constituency import is_candidate_eligible

eligible = is_candidate_eligible(
    constituency_type="SC",
    candidate_category="SC",
)
# eligible == True

eligible = is_candidate_eligible(
    constituency_type="SC",
    candidate_category="General",
)
# eligible == False (only SC candidates in SC seats)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `constituency_type` | str | `"General"`, `"SC"`, or `"ST"` |
| `candidate_category` | str | Candidate's demographic category |
| `reserved_map` | `dict[str, str] \| None` | Optional override mapping category → allowed types |

**Returns:** `bool` — `True` if candidate is eligible.

**Logic:**
- `"General"` constituencies: all candidates eligible
- Reserved constituencies (`"SC"`/`"ST"`): only candidates of matching category can contest
- If `reserved_map` is provided, it overrides the default mapping

**Example:**
```python
# Custom reservation rules
custom_map = {"SC": ["SC", "General"], "ST": ["ST"]}

is_candidate_eligible("SC", "General", reserved_map=custom_map)
# True — custom map allows General candidates in SC seats
```
