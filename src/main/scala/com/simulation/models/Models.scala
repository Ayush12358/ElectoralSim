package com.simulation.models

case class Ideology(dimensions: Seq[Double])

case class VoterAgent(
    id: String,
    ideology: Ideology,
    patronageAffinity: Double = 0.0 // 0.0 = pure ideology, 1.0 = pure patronage
)

case class Party(
    id: String,
    ideology: Ideology,
    patronageScore: Double = 0.5 // How much "benefits" this party offers [0, 1]
)
