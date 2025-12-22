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
   * Generates ideology clustered around a center point
   */
  def generateClusteredIdeology(nDim: Int, center: Seq[Double], spread: Double, rand: Random): Ideology = {
    val dims = center.map { c =>
      math.max(0.0, math.min(1.0, c + (rand.nextGaussian() * spread)))
    }
    Ideology(dims)
  }

  /**
   * Calculates vote choice with Clientelism blending
   * score = (1 - patronageAffinity) * ideologyScore + patronageAffinity * patronageScore
   */
  def calculateVoteScore(voter: VoterAgent, party: Party): Double = {
    val ideologyScore = 1.0 - calculateDistance(voter.ideology, party.ideology) // Higher = better
    val patronageScore = party.patronageScore
    (1.0 - voter.patronageAffinity) * ideologyScore + voter.patronageAffinity * patronageScore
  }

  /**
   * Coalition Formation: Minimum Connected Winning (MCW)
   * 
   * Strategy: Start from the largest party, then add ideologically CLOSEST parties
   * until majority is reached. This prevents unrealistic coalitions between
   * ideological opposites (e.g., far-left + far-right).
   * 
   * Literature: Axelrod (1970), De Swaan (1973), Laver & Shepsle (1996)
   */
  def formCoalition(seats: Map[String, Int], parties: Map[String, Party], threshold: Int): Set[String] = {
    if (seats.isEmpty) return Set.empty
    
    // Step 1: Start with the largest party (the formateur)
    val formateur = seats.maxBy(_._2)._1
    val formateurIdeology = parties(formateur).ideology
    
    // Step 2: Sort all other parties by ideological distance from formateur
    val otherParties = seats.filterNot(_._1 == formateur).toSeq.sortBy { case (partyId, _) =>
      calculateDistance(parties(partyId).ideology, formateurIdeology)
    }
    
    // Step 3: Build coalition by adding closest parties until threshold reached
    var coalition = Set(formateur)
    var currentSeats = seats(formateur)
    
    for ((partyId, s) <- otherParties if currentSeats < threshold) {
      coalition += partyId
      currentSeats += s
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
