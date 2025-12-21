package com.simulation.utils

import com.simulation.models.{VoterAgent, Ideology}
import scala.io.Source
import java.io.File

object DataIngestion {

  /**
   * Mock parser for IHDS/ECI CSV data
   * Expecting columns: id, age, caste, religion, urban, econ, social, regional, constituency
   */
  def loadVotersFromCSV(filePath: String): List[VoterAgent] = {
    if (!new File(filePath).exists()) {
      println(s"Warning: Data file $filePath not found. Falling back to synthetic generation.")
      Nil
    } else {
      val source = Source.fromFile(filePath)
      val lines = source.getLines().drop(1) // Header
      val voters = lines.map { line =>
        val cols = line.split(",").map(_.trim)
        VoterAgent(
          id = cols(0),
          age = cols(1).toInt,
          caste = cols(2),
          religion = cols(3),
          isUrban = cols(4).toBoolean,
          ideology = Ideology(cols(5).toDouble, cols(6).toDouble, cols(7).toDouble),
          constituencyId = cols(8)
        )
      }.toList
      source.close()
      voters
    }
  }
}
