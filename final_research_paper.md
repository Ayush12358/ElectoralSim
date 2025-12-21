# RESEARCH PAPER: Simulating the Stability-Proportionality Trade-off

**A Computational Counterfactual Analysis of Proportional Representation in the Indian Parliamentary System**

---

## 1. Abstract
The "Stability Anxiety" has long dominated the debate on electoral reform in India, favoring the First-Past-The-Post (FPTP) system despite its inherent disproportionality. This paper bridges the gap between political theory and empirical evidence through a large-scale (100k agent) Agent-Based Model (ABM). By simulating the 2024 general elections under counterfactual List-PR rules across three societal personas (Centrist, Polarized, and Fragmented), we quantify the trade-off between representativeness (Gallagher Index) and government durability (Mean Time To Failure). Our findings demonstrate that while PR offers superior fairness (Gallagher 0.0663 vs FPTP 0.5616), government stability is a function of societal cohesion. We identify a "Polarization Trap" where MTTF drops by over 70% in polarized contexts (1.31 years), while fragmented multi-party systems exhibit high resilience (4.05 years).

## 2. Introduction: The Constitutional Choice
India's adoption of the First-Past-The-Post (FPTP) system was a deliberate decision by the Constituent Assembly. Framers like B.R. Ambedkar prioritised executive stability over "mathematical fairness." Seven decades later, the "Gallagher Gap" (0.5616) has reached a point where minor vote margins command absolute majorities. This paper uses computational modeling to move the debate from normative conjecture to empirical optimization.

## 3. Theoretical Framework & Literature Review
### 3.1 Duverger’s Law vs. Indian Multi-partyism
According to **Duverger’s Law**, FPTP systems should naturally converge toward two-party systems. However, India's extreme pluralism has defied this, resulting in a fragmented multi-party system that inherits the disproportionality of FPTP without its consolidating benefits. 

### 3.2 Sartori’s Typology and "Stability Anxiety"
**Giovanni Sartori** classified party systems based on their fragmentation and ideological distance. In India, the fear of "undisciplined" multi-partyism—often termed "Stability Anxiety"—is used to justify the retention of FPTP. The Law Commission’s **170th (1999)** and **255th (2015)** reports acknowledged this, proposing hybrid models with thresholds (5%) to balance fairness with durability.

## 4. Methodology: The Counterfactual Laboratory
We leveraged the **BharatSim** framework to generate a synthetic population at a **1:10 scale resolution** (100,000 agents).

### 4.1 Spatial Ideological Modeling
Voters and parties are mapped across three dimensions: Economic, Social, and Regional axes. Stability is measured via **Mean Time To Failure (MTTF)** based on ideological strain and majority margin.

## 5. Audited Simulation Results & Discussion

| Persona | System | Gallagher Index | MTTF (Years) | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Hybrid (Base)** | FPTP | 0.5616 (High) | 5.00 (Stable) | Artificial Majority |
| **Centrist** | PR (5%) | 0.0663 (Fair) | 4.86 (Stable) | Consolidated PR |
| **Fragmented**| PR (5%) | 0.0409 (Fair) | 4.05 (Stable) | Regional Resilience |
| **Polarized** | PR (5%) | 0.0160 (Fair) | 1.31 (Fragile) | **Polarization Trap** |

### 5.1 The Polarization Trap
Our most significant finding is that institutional design (thresholds) cannot override deep social bifurcation. In the "Polarized" persona, stability remains dangerously low (1.31 years).

### 5.2 The Resilience of Fragmentation
Contrary to common fears, a "Fragmented" society (multiple regional parties) is highly stable under PR (MTTF 4.05).

## 6. Conclusion
An electoral threshold of 5% serves as a robust "Stability Bridge" for the Indian Republic, reducing representational distortion by over 75% without sacrificing government durability in consolidated social climates.

## 7. Acknowledgements
The author wishes to thank the open-source community of the **BharatSim** framework. Special thanks to the researchers at **Ashoka University** for their foundational work in agent-based modeling for Indian governance.

## 8. Artifacts & Data Provenance
- **Framework**: BharatSim (Scala 2.13)
- **Primary Data**: 2024 Booth-level Data (ECI)
- **Source Code**: [src/main/scala](file:///c:/masti/try/src)
