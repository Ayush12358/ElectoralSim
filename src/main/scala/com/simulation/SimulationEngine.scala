package com.simulation

import com.simulation.models.{Party, VoterAgent, Ideology}
import com.simulation.utils.ElectoralMath

object SimulationEngine {

  /**
   * Calculates the ideological distance between two entities
   */
  def calculateDistance(i1: Ideology, i2: Ideology): Double = {
    math.sqrt(
      math.pow(i1.economic - i2.economic, 2) +
      math.pow(i1.social - i2.social, 2) +
      math.pow(i1.regional - i2.regional, 2)
    )
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
      distances.sum / distances.size
    }
  }

  /**
   * Applies a policy shock to the ideological space
   */
  def applyPolicyShock(baseIdeology: Ideology, magnitude: Double, dimension: String): Ideology = {
    dimension.toLowerCase match {
      case "economic" => baseIdeology.copy(economic = math.max(0.0, math.min(1.0, baseIdeology.economic + magnitude)))
      case "social"   => baseIdeology.copy(social = math.max(0.0, math.min(1.0, baseIdeology.social + magnitude)))
      case "regional" => baseIdeology.copy(regional = math.max(0.0, math.min(1.0, baseIdeology.regional + magnitude)))
      case _          => baseIdeology
    }
  }

  /**
   * Calculates Mean Time To Failure (MTTF)
   * Refined for Research: Accounts for Majority Margin and Coalition Complexity
   */
  def calculateMTTF(strain: Double, shockMagnitude: Double, totalSeats: Int, govSeats: Int, isCoalition: Boolean): Double = {
    // 1. Base Risk from Ideology and Shocks
    val baseRisk = strain + (shockMagnitude * 0.4)
    
    // 2. Fragmented Majority Penalty: Government with razor-thin majority is more fragile
    val majorityRatio = govSeats.toDouble / totalSeats
    val marginBonus = math.max(0.0, (majorityRatio - 0.5) * 2.0) // Bonus for safe majorities
    
    // 3. Coalition Complexity Penalty (Reduced for realism)
    val coalitionPenalty = if (isCoalition) 0.05 else 0.0
    
    val totalRisk = baseRisk + (0.15 * (1.0 - marginBonus)) + coalitionPenalty
    
    // 4. Transform Risk to Years (Scale 0.5 to 5.0)
    // Adjusted center (1.0) and slope (3.0) for the 12-party high-strain environment
    val years = 5.5 / (1.0 + math.exp(3.5 * (totalRisk - 1.1)))
    math.max(0.5, math.min(5.0, years))
  }
}
