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
