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
Coalition & Government — verify formation, strain, and stability.

Mirrors README Coalition Formation snippet.
"""

import numpy as np
from electoral_sim import (
    form_government,
    coalition_strain,
    minimum_winning_coalitions,
    minimum_connected_winning,
    collapse_probability,
    simulate_government_survival,
)


def test_coalition_formation():
    """form_government returns expected keys."""
    seats = np.array([150, 120, 80, 50])
    positions = np.array([0.6, -0.3, 0.1, -0.6])
    names = ["Right", "Left", "Center", "Far-Left"]

    gov = form_government(seats, positions, names)
    assert "coalition_names" in gov
    assert "seats" in gov
    assert gov["seats"] > np.sum(seats) / 2  # Majority


def test_coalition_strain():
    """coalition_strain returns float."""
    positions = np.array([[0.6, 0.0], [-0.3, 0.0], [0.1, 0.0]])
    strain = coalition_strain(positions)
    assert isinstance(strain, float)
    assert strain >= 0


def test_mwc_and_mcw():
    """MWC and MCW find valid coalitions."""
    seats = np.array([40, 30, 20, 10])
    positions = np.array([[0.5, 0.0], [-0.2, 0.0], [0.1, 0.0], [-0.8, 0.0]])

    mwcs = minimum_winning_coalitions(seats)
    assert len(mwcs) > 0
    for coalition, total in mwcs:
        assert total >= 51

    mcws = minimum_connected_winning(seats, positions)
    assert isinstance(mcws, list)


def test_government_survival():
    """simulate_government_survival runs without error."""
    result = simulate_government_survival(
        strain=0.3,
        stability=0.7,
        model="sigmoid",
        max_term=30,
        n_simulations=100,
        seed=42,
    )
    assert "mean_survival" in result


if __name__ == "__main__":
    test_coalition_formation()
    test_coalition_strain()
    test_mwc_and_mcw()
    test_government_survival()
    print("All coalition & government snippets: OK")
