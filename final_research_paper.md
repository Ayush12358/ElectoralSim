# RESEARCH PAPER: Simulating the Stability-Proportionality Trade-off

**A Computational Counterfactual Analysis of Proportional Representation in the Indian Parliamentary System**

---

## 1. Abstract
The "Stability Anxiety" has long dominated the debate on electoral reform in India, favoring the First-Past-The-Post (FPTP) system despite its inherent disproportionality. This paper bridges the gap between political theory and empirical evidence through a large-scale (100k agent) Agent-Based Model (ABM). By simulating the 2024 general elections under counterfactual List-PR rules across three societal personas (Centrist, Polarized, and Fragmented), we quantify the trade-off between representativeness (Gallagher Index) and government durability (Mean Time To Failure). Our findings demonstrate that while PR offers superior fairness (Gallagher 0.0663 vs FPTP 0.2728), government stability is a function of societal cohesion. We identify a "Polarization Trap" where MTTF drops by over 70% in polarized contexts (1.31 years). Conversely, fragmented multi-party systems exhibit high resilience (4.05 years), supporting the feasibility of moderate electoral thresholds.

## 2. Introduction: The Constitutional Choice
India's adoption of the First-Past-The-Post (FPTP) system was a deliberate decision by the Constituent Assembly. Framer B.R. Ambedkar prioritised executive stability over "mathematical fairness," fearing that Proportional Representation (PR) would lead to a fractured legislature unable to sustain a government. However, seven decades later, the "Gallagher Gap" (calculated at 0.2728 in our baseline) has reached a point where minor vote shifts can command absolute majorities, potentially alienating large segments of the electorate. This paper uses computational modeling to ask: Can institutional design (thresholds) provide a "Stability Bridge" in a PR-based India?

## 3. Literature Review
The Law Commission of India's **170th Report (1999)** and **255th Report (2015)** both acknowledged the need for better proportionality but warned against "Stability Anxiety." They proposed hybrid models with thresholds to balance these competing needs. Academic analysis by **E. Sridharan** highlights that Indian coalitions often form **Surplus Majority Coalitions** (redundant partners), suggesting that the Indian political culture has existing mechanisms to manage fragmentation. Furthermore, **Chhibber and Verma (2018)** argue that India's "Ideological State" is defined by deep cross-cutting cleavages, making representation accuracy paramount.

## 4. Methodology: The Counterfactual Laboratory
We leveraged the **BharatSim** framework to generate a synthetic population at a **1:10 scale resolution** (100,000 agents).
- **Spatial Model**: A Multidimensional Spatial Model defined by Economic (Statism), Social (Traditionalism), and Regional (Decentralization) axes.
- **Agent Personas**: Voters were generated across three socio-political scenarios: Centrist (consensus-seeking), Polarized (hollowed center), and Fragmented (multi-clustered regionalism).
- **Stress Testing**: Governments were subjected to stochastic "Policy Shocks" (0.2 magnitude) to measure the **Mean Time To Failure (MTTF)**.

## 5. Audited Simulation Results & Discussion

| Scenario | System | Gallagher Index | MTTF (Years) | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Hybrid (Base)** | FPTP | 0.2728 (High) | 5.00 (Stable) | Artificial Majority |
| **Centrist** | PR (5% Threshold) | 0.0663 (Fair) | 4.86 (Stable) | Consolidated PR |
| **Fragmented**| PR (5% Threshold) | 0.0409 (Fair) | 4.05 (Stable) | Regional Resilience |
| **Polarized** | PR (5% Threshold) | 0.0160 (Fair) | 1.31 (Fragile) | **Polarization Trap** |

### 5.1 The Polarization Trap
The simulation reveals that institutional design is secondary to societal sentiment. In the "Polarized" persona, even with a 5% threshold, the stability remains at a critical 1.31 years. This suggests that electoral reform alone cannot fix deep-seated societal rifts; the "Stability Bridge" requires a minimum level of consensus.

### 5.2 The Resilience of Fragmentation
Contrary to the "Stability Anxiety," our model shows that a "Fragmented" society (multiple regional parties) is highly stable under PR (MTTF 4.05). This matches the "Surplus Coalition" theory, proving that a diverse, multi-polar legislature is not inherently chaotic.

## 6. Conclusion
India can safely transition to a more representative democracy in stable social contexts using a 5% electoral threshold. Our model quantifies that this shift could reduce representational distortion by 75% while maintaining nearly a full term of stability in most scenarios.

---

## 7. Artifacts
- **Framework**: BharatSim (Scala/ABM)
- **Primary Data**: 2024 Booth-level Data (ECI) & IHDS-II
- **Source Code**: [src/main/scala](file:///c:/masti/try/src)
