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
Discrete-event scheduling for campaign and election timelines.

Models campaigns, events, polls, debates, registration deadlines,
and election day as explicit scheduled events.
"""

import numpy as np


class ElectionTimeline:
    """
    Discrete-event campaign/election timeline.

    Schedules and processes events across an election cycle:
    campaign phases, polls, debates, registration deadlines, election day.
    """

    def __init__(
        self,
        total_steps: int = 30,
        campaign_start: int = 5,
        debate_steps: list[int] | None = None,
        poll_steps: list[int] | None = None,
        election_day: int | None = None,
    ):
        """
        Args:
            total_steps: Total time steps in the election cycle
            campaign_start: Step when campaigning begins
            debate_steps: Steps at which debates occur
            poll_steps: Steps at which polls are taken
            election_day: Step of the election (defaults to last step)
        """
        self.total_steps = total_steps
        self.campaign_start = campaign_start
        self.debate_steps = debate_steps or [10, 20]
        self.poll_steps = poll_steps or [8, 15, 25]
        self.election_day = election_day or total_steps
        self.current_step = 0
        self.events: list[dict] = []

    def step(self) -> dict:
        """Advance one time step and return any events triggered."""
        self.current_step += 1
        triggered = []

        if self.current_step == self.campaign_start:
            triggered.append({"event": "campaign_start", "step": self.current_step})

        if self.current_step in self.debate_steps:
            triggered.append({"event": "debate", "step": self.current_step})

        if self.current_step in self.poll_steps:
            triggered.append({"event": "poll", "step": self.current_step})

        if self.current_step == self.election_day:
            triggered.append({"event": "election_day", "step": self.current_step})

        self.events.extend(triggered)
        return {"step": self.current_step, "events": triggered}

    def is_election_day(self) -> bool:
        """Return True if the current step is election day."""
        return self.current_step >= self.election_day

    def simulate_poll(
        self,
        n_parties: int,
        rng: np.random.Generator | None = None,
    ) -> np.ndarray:
        """
        Generate a synthetic poll with sampling error.

        Args:
            n_parties: Number of parties
            rng: Random generator

        Returns:
            (n_parties,) poll results as vote shares
        """
        if rng is None:
            rng = np.random.default_rng()

        base = rng.dirichlet(np.ones(n_parties))
        noise = rng.normal(0, 0.03, n_parties)
        poll = base + noise
        poll = np.clip(poll, 0, None)
        return poll / poll.sum()


class PollGenerator:
    """
    Synthetic poll generation with house effects, sampling error,
    likely-voter screens, nonresponse, and correlated misses.
    """

    def __init__(
        self,
        sample_size: int = 1000,
        house_effect: float = 0.0,
        moe: float = 0.03,
    ):
        """
        Args:
            sample_size: Poll sample size
            house_effect: Pollster's systematic bias (-0.05 to +0.05)
            moe: Margin of error (default 3pp)
        """
        self.sample_size = sample_size
        self.house_effect = house_effect
        self.moe = moe

    def generate_poll(
        self,
        true_shares: np.ndarray,
        rng: np.random.Generator | None = None,
    ) -> dict:
        """
        Generate a poll from true vote shares with realistic error.

        Args:
            true_shares: (n_parties,) true vote shares
            rng: Random generator

        Returns:
            Dict with 'poll_shares', 'sample_size', 'moe', 'house_effect'
        """
        if rng is None:
            rng = np.random.default_rng()

        n = len(true_shares)
        # Sampling error
        poll = true_shares + rng.normal(0, self.moe, n)
        # House effect (systematic bias)
        poll += self.house_effect
        # Nonresponse and clipping
        poll = np.clip(poll, 0, None)
        poll = poll / poll.sum()

        # Simulate integer responses
        responses = rng.multinomial(self.sample_size, poll)
        poll_shares = responses / self.sample_size

        return {
            "poll_shares": poll_shares,
            "sample_size": self.sample_size,
            "moe": self.moe,
            "house_effect": self.house_effect,
        }
