package com.simulation

import com.simulation.models._
import com.simulation.utils.ElectoralMath
import scala.util.Random
import java.io.PrintWriter
import java.io.File

object CounterfactualMain extends App {
  // Monte Carlo Configuration
  val nAgents = 10000
  val nTrials = 30    // Reduced for faster iteration with more params
  val totalSeats = 500
  val rangeDimensions = Seq(2, 3, 5, 8)
  val rangeParties = Seq(5, 8, 12, 20)
  val rangeThresholds = Seq(0.0, 0.05, 0.10)
  val rangePatronage = Seq(0.0, 0.3, 0.6, 0.9) // NEW: Clientelism sweep
  val polarizationTypes = Seq("Uniform", "Symmetric", "Asymmetric") // NEW
  
  println(s"--- Starting Extended Monte Carlo Simulation ---")
  println(s"Patronage Levels: $rangePatronage")
  println(s"Polarization Types: $polarizationTypes")

  val csvWriter = new PrintWriter(new File("data/processed/extended_theory_results.csv"))
  csvWriter.println("dimensions,n_parties,threshold,patronage,polarization,avg_mttf,avg_gallagher,std_mttf")

  val rand = new Random(42)

  // Simulation Loop
  for {
    dim <- rangeDimensions
    nP <- rangeParties
    thresh <- rangeThresholds
    patronageLevel <- rangePatronage
    polType <- polarizationTypes
  } {
    var rawMTTF = Seq.empty[Double]
    var rawGallagher = Seq.empty[Double]

    for (_ <- 1 to nTrials) {
      // 1. Generate Parties with random patronage scores
      val parties = (1 to nP).map { i => 
        val p = Party(
          s"P$i", 
          SimulationEngine.generateRandomIdeology(dim, rand),
          rand.nextDouble() // Random patronage score for each party
        )
        p.id -> p
      }.toMap

      // 2. Generate Voters based on polarization type
      val voters = polType match {
        case "Uniform" =>
          (1 to nAgents).map { i =>
            VoterAgent(s"V$i", SimulationEngine.generateRandomIdeology(dim, rand), patronageLevel)
          }
        case "Symmetric" =>
          // Two symmetric clusters at opposite corners
          val half = nAgents / 2
          val cluster1 = (1 to half).map { i =>
            val center = Seq.fill(dim)(0.2)
            VoterAgent(s"V$i", SimulationEngine.generateClusteredIdeology(dim, center, 0.1, rand), patronageLevel)
          }
          val cluster2 = ((half + 1) to nAgents).map { i =>
            val center = Seq.fill(dim)(0.8)
            VoterAgent(s"V$i", SimulationEngine.generateClusteredIdeology(dim, center, 0.1, rand), patronageLevel)
          }
          cluster1 ++ cluster2
        case "Asymmetric" =>
          // 80% in dominant pole, 20% scattered
          val dominant = (nAgents * 0.8).toInt
          val cluster1 = (1 to dominant).map { i =>
            val center = Seq.fill(dim)(0.85) // Dominant extreme pole
            VoterAgent(s"V$i", SimulationEngine.generateClusteredIdeology(dim, center, 0.08, rand), patronageLevel)
          }
          val scattered = ((dominant + 1) to nAgents).map { i =>
            VoterAgent(s"V$i", SimulationEngine.generateRandomIdeology(dim, rand), patronageLevel)
          }
          cluster1 ++ scattered
      }

      // 3. Cast Votes using blended score (ideology + patronage)
      val votes = voters.map { v =>
        val bestParty = parties.values.maxBy(p => SimulationEngine.calculateVoteScore(v, p))
        bestParty.id
      }.groupBy(identity).mapValues(_.size)

      // 4. Allocate Seats
      val totalVotes = votes.values.sum
      val qualifiedVotes = votes.filter { case (_, v) => (v.toDouble / totalVotes) >= thresh }
      val seats = ElectoralMath.allocateSainteLague(qualifiedVotes.toMap, totalSeats)

      // 5. Form Coalition & Calculate Stability
      val maxSeatParty = if (seats.nonEmpty) seats.maxBy(_._2) else ("None" -> 0)
      val govSeats = if (maxSeatParty._2 > 250) {
          maxSeatParty._2
      } else {
          val coal = SimulationEngine.formCoalition(seats, parties, 251)
          coal.toList.map(seats.getOrElse(_, 0)).sum
      }
      val isCoalition = maxSeatParty._2 <= 250

      val coalitionSet = if (!isCoalition) Set(maxSeatParty._1) else SimulationEngine.formCoalition(seats, parties, 251)
      val strain = SimulationEngine.calculateStrain(coalitionSet, parties)
      
      val mttf = SimulationEngine.calculateMTTF(strain, 0.2, totalSeats, govSeats, isCoalition)
      val gallagher = ElectoralMath.calculateGallagherIndex(
        votes.mapValues(_.toDouble/totalVotes).toMap, 
        seats.mapValues(_.toDouble/totalSeats).toMap
      )
      
      rawMTTF = rawMTTF :+ mttf
      rawGallagher = rawGallagher :+ gallagher
    }

    // Aggregation
    val avgMTTF = rawMTTF.sum / nTrials
    val avgGallagher = rawGallagher.sum / nTrials
    val stdMTTF = math.sqrt(rawMTTF.map(x => math.pow(x - avgMTTF, 2)).sum / nTrials)

    csvWriter.println(f"$dim,$nP,$thresh,$patronageLevel,$polType,$avgMTTF,$avgGallagher,$stdMTTF")
  }

  csvWriter.close()
  println("Extended Simulation Complete. Results saved to data/processed/extended_theory_results.csv")
}
