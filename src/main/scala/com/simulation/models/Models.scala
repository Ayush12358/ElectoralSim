package com.simulation.models

case class Ideology(economic: Double, social: Double, regional: Double)

case class VoterAgent(
    id: String,
    age: Int,
    caste: String,
    religion: String,
    isUrban: Boolean,
    ideology: Ideology,
    constituencyId: String
)

case class Party(
    id: String,
    name: String,
    ideology: Ideology,
    isRegional: Boolean,
    baseRegion: Option[String] = None
)
