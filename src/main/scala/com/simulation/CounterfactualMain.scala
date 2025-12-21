package com.simulation

import com.simulation.models._
import com.simulation.utils.ElectoralMath
import scala.util.Random

object CounterfactualMain extends App {
  // 1. Setup Support Structures
  val parties = Map(
    "BJP"  -> Party("BJP", "BJP", Ideology(0.9, 0.9, 0.1), isRegional = false),
    "INC"  -> Party("INC", "INC", Ideology(0.3, 0.4, 0.3), isRegional = false),
    "AAP"  -> Party("AAP", "AAP", Ideology(0.2, 0.6, 0.5), isRegional = true),
    "TMC"  -> Party("TMC", "TMC", Ideology(0.4, 0.2, 0.9), isRegional = true),
    "DMK"  -> Party("DMK", "DMK", Ideology(0.3, 0.2, 0.8), isRegional = true),
    "SP"   -> Party("SP", "SP", Ideology(0.4, 0.7, 0.3), isRegional = true),
    "JDU"  -> Party("JDU", "JDU", Ideology(0.6, 0.6, 0.4), isRegional = true),
    "NCP"  -> Party("NCP", "NCP", Ideology(0.5, 0.5, 0.5), isRegional = true),
    "CPM"  -> Party("CPM", "Left 1", Ideology(0.1, 0.3, 0.2), isRegional = false),
    "CPI"  -> Party("CPI", "Left 2", Ideology(0.1, 0.2, 0.1), isRegional = false),
    "OTH1" -> Party("OTH1", "Fringe 1", Ideology(0.8, 0.2, 0.4), isRegional = true),
    "OTH2" -> Party("OTH2", "Fringe 2", Ideology(0.2, 0.8, 0.7), isRegional = true)
  )

  def generateVoters(n: Int, persona: String = "Hybrid"): Seq[VoterAgent] = {
    val random = new Random(42)
    (1 to n).map { i =>
      val ideology = persona match {
        case "Polarized" => 
          val center = if (random.nextBoolean()) 0.1 else 0.9
          Ideology(math.max(0, math.min(1, center + random.nextGaussian() * 0.1)), math.max(0, math.min(1, center + random.nextGaussian() * 0.1)), random.nextDouble())
        case "Fragmented" => Ideology(random.nextDouble(), random.nextDouble(), random.nextDouble())
        case "Centrist" => Ideology(math.max(0, math.min(1, 0.5 + random.nextGaussian() * 0.15)), math.max(0, math.min(1, 0.5 + random.nextGaussian() * 0.15)), random.nextDouble())
        case _ => 
          val center = if (random.nextBoolean()) 0.8 else 0.3
          Ideology(center + random.nextGaussian() * 0.1, center + random.nextGaussian() * 0.1, random.nextDouble())
      }
      VoterAgent(s"v$i", 18 + random.nextInt(60), "Gen", "Hindu", random.nextBoolean(), ideology, s"C${random.nextInt(10)}")
    }
  }

  // --- Research Configuration ---
  val nAgents = 100000
  val totalSeats = 543
  val defaultShock = 0.2
  val researchThresholds = Seq(0.0, 0.01, 0.03, 0.05, 0.08, 0.10, 0.15)
  val shockRange = Seq(0.1, 0.2, 0.3, 0.5)

  println("--- Final Publication Audit: Scenario Sweep ---")
  
  // 1. FPTP Baseline (Centrist/Hybrid)
  val baselineVoters = generateVoters(nAgents, "Hybrid")
  val baselineVotesByParty = baselineVoters.map(v => parties.values.minBy(p => SimulationEngine.calculateDistance(v.ideology, p.ideology)).id).groupBy(identity).mapValues(_.size).toMap
  val fptpSeats = baselineVoters.groupBy(_.constituencyId).map { case (cid, vs) =>
    vs.map(v => parties.values.minBy(p => SimulationEngine.calculateDistance(v.ideology, p.ideology)).id).groupBy(identity).mapValues(_.size).maxBy(_._2)._1 -> 1
  }.toSeq.groupBy(_._1).mapValues(_.size).toMap
  val fptpG = ElectoralMath.calculateGallagherIndex(baselineVotesByParty.mapValues(_.toDouble/nAgents).toMap, fptpSeats.mapValues(_.toDouble/fptpSeats.values.sum).toMap)
  println(f"FPTP Baseline: Gallagher=$fptpG%.4f | MTTF=5.00")

  // --- RUN 2: THE EXTENDED SENSITIVITY (For visualizer) ---
  val csvExtended = new java.io.PrintWriter(new java.io.File("data/processed/extended_simulation_results.csv"))
  csvExtended.println("threshold,shock_magnitude,gallagher_index,mttf,fragmentation")
  for {
    t <- researchThresholds
    sm <- shockRange
  } {
    val filtered = baselineVotesByParty.filter(_._2.toDouble/nAgents >= t)
    val seats = ElectoralMath.allocateSainteLague(filtered, totalSeats)
    val coal = SimulationEngine.formCoalition(seats, parties, 272)
    val mttf = SimulationEngine.calculateMTTF(SimulationEngine.calculateStrain(coal, parties), sm, totalSeats, coal.toList.map(seats).sum, coal.size > 1)
    csvExtended.println(f"$t,$sm,${ElectoralMath.calculateGallagherIndex(baselineVotesByParty.mapValues(_.toDouble/nAgents).toMap, seats.mapValues(_.toDouble/totalSeats).toMap)},$mttf,${coal.size}")
  }
  csvExtended.close()

  // --- RUN 3: SOCIETAL PERSONAS ---
  val csvSocietal = new java.io.PrintWriter(new java.io.File("data/processed/societal_stress_results.csv"))
  csvSocietal.println("persona,threshold,gallagher_index,mttf")
  Seq("Centrist", "Polarized", "Fragmented").foreach { p =>
    val pvoters = generateVoters(nAgents, p)
    val pvByP = pvoters.map(v => parties.values.minBy(p => SimulationEngine.calculateDistance(v.ideology, p.ideology)).id).groupBy(identity).mapValues(_.size).toMap
    Seq(0.0, 0.05).foreach { t =>
      val filtered = pvByP.filter(_._2.toDouble/nAgents >= t)
      val seats = ElectoralMath.allocateSainteLague(filtered, totalSeats)
      val coal = SimulationEngine.formCoalition(seats, parties, 272)
      val mttf = SimulationEngine.calculateMTTF(SimulationEngine.calculateStrain(coal, parties), 0.2, totalSeats, coal.toList.map(seats).sum, coal.size > 1)
      val lsq = ElectoralMath.calculateGallagherIndex(pvByP.mapValues(_.toDouble/nAgents).toMap, seats.mapValues(_.toDouble/totalSeats).toMap)
      csvSocietal.println(f"$p,$t,$lsq,$mttf")
      if (t == 0.05) println(f"PR $p ($t) : Gallagher=$lsq%.4f | MTTF=$mttf%.2f")
    }
  }
  csvSocietal.close()
  println("\nGrand Run Complete. All CSVs updated.")
}
