"""
Event Manager Module

Handles dynamic events such as scandals, economic shocks, and international crises
that affect election outcomes.
"""

from dataclasses import dataclass
from typing import Literal

import numpy as np


@dataclass
class Event:
    """represents a dynamic event in the simulation."""

    id: int
    type: Literal["scandal", "economic_shock", "international_crisis"]
    start_step: int
    duration: int
    severity: float  # 0.0 to 1.0 (or higher)
    target_party_id: int | None = None
    description: str = ""

    @property
    def end_step(self) -> int:
        return self.start_step + self.duration


class EventManager:
    """
    Manages generation and tracking of events.

    Attributes:
        active_events: List of currently active events
        history: List of past events
    """

    def __init__(
        self, rng: np.random.Generator, prob_scandal: float = 0.01, prob_shock: float = 0.005
    ):
        self.rng = rng
        self.prob_scandal = prob_scandal
        self.prob_shock = prob_shock
        self.active_events: list[Event] = []
        self.history: list[Event] = []
        self.event_counter = 0
        self.current_step = 0

    def step(self, n_parties: int) -> list[Event]:
        """
        Advance one step, potentially generating new events and expiring old ones.

        Returns:
            List of NEW events generated this step.
        """
        self.current_step += 1
        new_events = []

        # 1. Clean up expired events
        self.active_events = [e for e in self.active_events if e.end_step > self.current_step]

        # 2. Generate Scanals
        if self.rng.random() < self.prob_scandal:
            target = self.rng.integers(0, n_parties)
            severity = self.rng.beta(2, 5) * 50  # 0-50 valence penalty
            duration = self.rng.integers(3, 12)  # 3-12 months/steps

            event = Event(
                id=self.event_counter,
                type="scandal",
                start_step=self.current_step,
                duration=duration,
                severity=severity,
                target_party_id=target,
                description=f"Scandal hitting Party {target} (Severity: {severity:.1f})",
            )
            self.event_counter += 1
            self.active_events.append(event)
            self.history.append(event)
            new_events.append(event)

        # 3. Generate Economic Shocks
        if self.rng.random() < self.prob_shock:
            # Positive or negative shock?
            # 70% negative (crises), 30% positive (booms)
            is_negative = self.rng.random() < 0.7
            magnitude = self.rng.beta(2, 5) * 5.0  # Up to 5% GDP shift
            severity = -magnitude if is_negative else magnitude
            duration = self.rng.integers(6, 24)

            event = Event(
                id=self.event_counter,
                type="economic_shock",
                start_step=self.current_step,
                duration=duration,
                severity=severity,
                target_party_id=None,  # Affects incumbent usually
                description=f"Economic {'Crash' if is_negative else 'Boom'} ({severity:.1f}%)",
            )
            self.event_counter += 1
            self.active_events.append(event)
            self.history.append(event)
            new_events.append(event)

        return new_events

    def get_valence_modifiers(self) -> dict[int, float]:
        """
        Get total valence penalty/bonus for each party from active events.
        """
        modifiers = {}
        for event in self.active_events:
            if event.type == "scandal" and event.target_party_id is not None:
                # Decay effect over time?
                # Simple linear decay: full severity at start, 0 at end
                progress = (self.current_step - event.start_step) / event.duration
                current_impact = -event.severity * (1.0 - progress)

                pid = event.target_party_id
                modifiers[pid] = modifiers.get(pid, 0.0) + current_impact

        return modifiers

    def get_economic_modifier(self) -> float:
        """
        Get total modification to economic growth from active shocks.
        """
        total_shock = 0.0
        for event in self.active_events:
            if event.type == "economic_shock":
                # Decay
                progress = (self.current_step - event.start_step) / event.duration
                current_impact = event.severity * (1.0 - progress)
                total_shock += current_impact
        return total_shock
