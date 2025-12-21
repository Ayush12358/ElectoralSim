package com.simulation.models

case class Ideology(dimensions: Seq[Double])

case class VoterAgent(
    id: String,
    ideology: Ideology,
    constituencyId: String = "C1" // Default for abstract model
)

case class Party(
    id: String,
    ideology: Ideology
)
