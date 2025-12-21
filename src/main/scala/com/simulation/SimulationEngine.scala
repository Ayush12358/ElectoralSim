package com.simulation

import com.simulation.models.{Party, VoterAgent, Ideology}
import com.simulation.utils.ElectoralMath
import scala.util.Random

object SimulationEngine {

  /**
   * Calculates Euclidean distance in N-dimensions
   */
  def calculateDistance(i1: Ideology, i2: Ideology): Double = {
    math.sqrt(
      i1.dimensions.zip(i2.dimensions).map { case (d1, d2) => math.pow(d1 - d2, 2) }.sum
    )
  }

  /**
   * Generates a random N-dimensional ideology
   */
  def generateRandomIdeology(nDim: Int, rand: Random = new Random()): Ideology = {
    Ideology(Seq.fill(nDim)(rand.nextDouble()))
  }

  /**
   * Simple Coalition Formation: Minimum Winning Coalition (MWC)
   */
  def formCoalition(seats: Map[String, Int], parties: Map[String, Party], threshold: Int): Set[String] = {
    val sortedParties = seats.toSeq.sortBy(-_._2)
    var currentSeats = 0
    var coalition = Set.empty[String]
    
    for ((partyId, s) <- sortedParties) {
      if (currentSeats < threshold) {
        currentSeats += s
        coalition += partyId
      }
    }
    coalition
  }

  /**
   * Calculates Coalition Ideological Strain
   */
  def calculateStrain(coalition: Set[String], parties: Map[String, Party]): Double = {
    if (coalition.size <= 1) 0.0
    else {
      val ids = coalition.toList
      val distances = for {
        p1 <- ids
        p2 <- ids if p1 < p2
      } yield calculateDistance(parties(p1).ideology, parties(p2).ideology)
      if (distances.isEmpty) 0.0 else distances.sum / distances.size
    }
  }

  /**
   * Calculates Mean Time To Failure (MTTF) - Generalized
   */
  def calculateMTTF(strain: Double, shockMagnitude: Double, totalSeats: Int, govSeats: Int, isCoalition: Boolean): Double = {
    val baseRisk = strain + (shockMagnitude * 0.4)
    val majorityRatio = govSeats.toDouble / totalSeats
    val marginBonus = math.max(0.0, (majorityRatio - 0.5) * 2.0)
    val coalitionPenalty = if (isCoalition) 0.05 else 0.0
    val totalRisk = baseRisk + (0.15 * (1.0 - marginBonus)) + coalitionPenalty
    val years = 5.5 / (1.0 + math.exp(3.5 * (totalRisk - 1.1)))
    math.max(0.5, math.min(5.0, years))
  }
}
