# ElectoralSim: Live Demo Script

**Total Duration**: ~5 Minutes
**Prerequisite**: Ensure the app is running: `streamlit run app.py`

---

## Phase 1: The Hook (Scale & Speed)
**Action**: Open the App. Select "India (Lok Sabha)".
**Say**:
> "This isn't just a static chart. We are about to simulate the voting behavior of a representative sample of the specific diverse electorate of India."

**Action**: set "Voter Sample Size" to **50,000**. Click **Run Simulation**.
**Say**:
> "In just a few milliseconds, the engine generated 50,000 unique agents, calculated their distances to 10+ parties, applied strategic voting logic, and aggregated the results across 543 constituencies."

---

## Phase 2: The "What-If" Analysis (Interactivity)
**Action**: Scroll to "Election Outcome". Point out the "Winning Party".
**Say**:
> "Here we see the baseline result. But elections are dynamic. Let's simulate a 'Wave Election'."

**Action**: Go to Sidebar > **Dynamic Parameters**.
1.  Set **National Mood** to `+2.0` (In favor of incumbents) or `-2.0` (Anti-incumbency wave).
2.  Click **Run Simulation** again.

**Action**: Show the **Swing Analysis** chart at the bottom.
**Say**:
> "Notice how a small shift in voter sentiment (the 'National Mood') disproportionately affects the seat count. This demonstrates the 'Winner's Bonus' inherent in the FPTP system used in India."

---

## Phase 3: Fairness & Metrics (Depth)
**Action**: Scroll to **Seats vs Votes Disproportionality**.
**Say**:
> "One key question in political science is: Is the result fair? Did the party with 30% votes get 30% seats?"

**Action**: Point to the **Gallagher Index** metric at the top.
**Say**:
> "We calculate the Gallagher Index automatically. A lower score is 'fairer'. Compare this to a Proportional system like Germany (Select Preset: Germany), and you'll see this number drop significantly."

---

## Phase 4: Closing
**Say**:
> "ElectoralSim allows us to move beyond intuition and test these democratic mechanisms rigorously with data. Any questions?"
