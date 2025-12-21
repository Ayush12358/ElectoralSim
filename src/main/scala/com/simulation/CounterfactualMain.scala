package com.simulation

import com.simulation.models._
import com.simulation.utils.ElectoralMath
import scala.util.Random
import java.io.PrintWriter
import java.io.File

object CounterfactualMain extends App {
  // Monte Carlo Configuration
  val nAgents = 10000 // 10k agents is sufficient for statistical convergence
  val nTrials = 50    // 50 random party constellations per config
  val totalSeats = 500
  val rangeDimensions = Seq(2, 3, 4, 5, 8)
  val rangeParties = Seq(3, 5, 8, 12, 16, 20)
  val rangeThresholds = Seq(0.0, 0.03, 0.05, 0.10)
  
  println(s"--- Starting General Theory Monte Carlo Simulation ---")
  println(s"Dimensions: $rangeDimensions")
  println(s"Parties: $rangeParties")
  println(s"Thresholds: $rangeThresholds")
  println(s"Trials per Config: $nTrials")

  val csvWriter = new PrintWriter(new File("data/processed/general_theory_results.csv"))
  csvWriter.println("dimensions,n_parties,threshold,avg_mttf,avg_gallagher,std_mttf,std_gallagher")

  val rand = new Random(42)

  // Simulation Loop
  for {
    dim <- rangeDimensions
    nP <- rangeParties
    thresh <- rangeThresholds
  } {
    var rawMTTF = Seq.empty[Double]
    var rawGallagher = Seq.empty[Double]

    for (_ <- 1 to nTrials) {
      // 1. Generate Random Environment
      val parties = (1 to nP).map { i => 
        val p = Party(s"P$i", SimulationEngine.generateRandomIdeology(dim, rand))
        p.id -> p
      }.toMap
      
      val voters = (1 to nAgents).map { i =>
        VoterAgent(s"V$i", SimulationEngine.generateRandomIdeology(dim, rand))
      }

      // 2. Cast Votes (Proximity Voting)
      val votes = voters.map { v =>
        val bestParty = parties.values.minBy(p => SimulationEngine.calculateDistance(v.ideology, p.ideology))
        bestParty.id
      }.groupBy(identity).mapValues(_.size)

      // 3. Allocate Seats (Sainte-Lague)
      // Filter by threshold first
      val totalVotes = votes.values.sum
      val qualifiedVotes = votes.filter { case (_, v) => (v.toDouble / totalVotes) >= thresh }
      val seats = ElectoralMath.allocateSainteLague(qualifiedVotes.toMap, totalSeats)

      // 4. Form Coalition & Calculate Stability
      // Majority needed = 251. If no one has 251, form coalition.
      val maxSeatParty = if (seats.nonEmpty) seats.maxBy(_._2) else ("None" -> 0)
      val govSeats = if (maxSeatParty._2 > 250) {
          // Single party majority
          maxSeatParty._2
      } else {
          // Coalition needed
          val coal = SimulationEngine.formCoalition(seats, parties, 251)
          coal.toList.map(seats.getOrElse(_, 0)).sum
      }
      val isCoalition = maxSeatParty._2 <= 250

      val coalitionSet = if (!isCoalition) Set(maxSeatParty._1) else SimulationEngine.formCoalition(seats, parties, 251)
      val strain = SimulationEngine.calculateStrain(coalitionSet, parties)
      
      // Calculate Metrics
      val mttf = SimulationEngine.calculateMTTF(strain, 0.2, totalSeats, govSeats, isCoalition)
      val gallagher = ElectoralMath.calculateGallagherIndex(votes.mapValues(_.toDouble/totalVotes).toMap, seats.mapValues(_.toDouble/totalSeats).toMap)
      
      rawMTTF = rawMTTF :+ mttf
      rawGallagher = rawGallagher :+ gallagher
    }

    // Aggregation
    val avgMTTF = rawMTTF.sum / nTrials
    val avgGallagher = rawGallagher.sum / nTrials
    val stdMTTF = math.sqrt(rawMTTF.map(x => math.pow(x - avgMTTF, 2)).sum / nTrials)
    val stdGallagher = math.sqrt(rawGallagher.map(x => math.pow(x - avgGallagher, 2)).sum / nTrials)

    // println(f"Dim=$dim, Parties=$nP, T=$thresh%2.2f -> MTTF=$avgMTTF%2.2f, Gallagher=$avgGallagher%4.4f")
    csvWriter.println(f"$dim,$nP,$thresh,$avgMTTF,$avgGallagher,$stdMTTF,$stdGallagher")
  }

  csvWriter.close()
  println("Simulation Complete. Results saved to data/processed/general_theory_results.csv")
}
