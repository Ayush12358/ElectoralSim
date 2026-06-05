#!/usr/bin/env python

# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Duverger's Law Experiment — FPTP vs PR effective number of parties.

Duverger's Law predicts that FPTP systems converge toward two-party dominance
while PR systems maintain multi-party diversity. This demo runs both systems
side-by-side and compares the effective number of parties (ENP) over time.

Run:
    python examples/duverger_demo.py
"""

from electoral_sim.analysis.duverger import run_duverger_experiment


def main():
    print("=" * 60)
    print("Duverger's Law: FPTP vs PR — Effective Number of Parties")
    print("=" * 60)

    # Run FPTP experiment (should converge to ~2 parties)
    print("\n[FPTP] Running with strategic voting...")
    fptp_history = run_duverger_experiment(
        n_voters=2000,
        n_parties=5,
        n_steps=10,
        system="FPTP",
        seed=42,
    )

    # Run PR experiment (should maintain ~5 parties)
    print("\n[PR] Running with strategic voting...")
    pr_history = run_duverger_experiment(
        n_voters=2000,
        n_parties=5,
        n_steps=10,
        system="PR",
        seed=42,
    )

    # Compare results
    print("\n" + "=" * 60)
    print("Results: Step | FPTP ENP | PR ENP")
    print("-" * 60)
    for i, (f, p) in enumerate(zip(fptp_history, pr_history)):
        print(f"  {f['step']:>4}  |   {f['enp']:.2f}   |  {p['enp']:.2f}")

    enp_fptp = fptp_history[-1]["enp"]
    enp_pr = pr_history[-1]["enp"]
    print("-" * 60)
    print(f"Final FPTP ENP: {enp_fptp:.2f} (Expected: ~2.0)")
    print(f"Final PR ENP:   {enp_pr:.2f} (Expected: ~5.0)")
    print()

    if enp_fptp < enp_pr:
        print("Duverger's Law confirmed: FPTP has fewer effective parties than PR.")
    else:
        print("Result: FPTP did not converge below PR in this run. Try more steps.")


if __name__ == "__main__":
    main()
