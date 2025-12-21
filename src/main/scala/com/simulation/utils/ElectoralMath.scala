package com.simulation.utils

import com.simulation.models.Party

object ElectoralMath {

  /**
   * Calculates the Gallagher Index (LSq)
   * LSq = sqrt(0.5 * sum((voteShare - seatShare)^2))
   */
  def calculateGallagherIndex(voteShares: Map[String, Double], seatShares: Map[String, Double]): Double = {
    val totalDiffSquared = voteShares.keys.map { partyId =>
      val v = voteShares.getOrElse(partyId, 0.0)
      val s = seatShares.getOrElse(partyId, 0.0)
      math.pow(v - s, 2)
    }.sum
    math.sqrt(0.5 * totalDiffSquared)
  }

  /**
   * D'Hondt Seat Allocation
   */
  def allocateDHondt(votes: Map[String, Int], totalSeats: Int): Map[String, Int] = {
    var seats = votes.keys.map(_ -> 0).toMap
    for (_ <- 1 to totalSeats) {
      val winner = votes.maxBy { case (partyId, v) =>
        v.toDouble / (seats(partyId) + 1)
      }._1
      seats = seats + (winner -> (seats(winner) + 1))
    }
    seats
  }

  /**
   * Sainte-Laguë Seat Allocation
   */
  def allocateSainteLague(votes: Map[String, Int], totalSeats: Int): Map[String, Int] = {
    var seats = votes.keys.map(_ -> 0).toMap
    for (_ <- 1 to totalSeats) {
      val winner = votes.maxBy { case (partyId, v) =>
        v.toDouble / (2 * seats(partyId) + 1)
      }._1
      seats = seats + (winner -> (seats(winner) + 1))
    }
    seats
  }
}
