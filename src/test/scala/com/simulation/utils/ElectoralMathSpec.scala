package com.simulation.utils

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class ElectoralMathSpec extends AnyFlatSpec with Matchers {

  "D'Hondt allocation" should "correctly allocate seats for a simple case" in {
    val votes = Map("A" -> 100, "B" -> 80, "C" -> 30)
    val totalSeats = 8
    val result = ElectoralMath.allocateDHondt(votes, totalSeats)
    
    // Manual calculation check:
    // A: 100/1=100 (1), 100/2=50 (3), 100/3=33.3 (5), 100/4=25 (7) -> 4 seats
    // B: 80/1=80 (2), 80/2=40 (4), 80/3=26.6 (8) -> 3 seats
    // C: 30/1=30 (6) -> 1 seat
    result("A") shouldBe 4
    result("B") shouldBe 3
    result("C") shouldBe 1
  }

  "Sainte-Laguë allocation" should "be more favorable to small parties" in {
    val votes = Map("A" -> 100, "B" -> 20)
    val totalSeats = 3
    
    // D'Hondt for comparison: A:100/1=100, 100/2=50, 100/3=33. B:20/1=20. Seats: A=3, B=0
    // Sainte-Laguë: 
    // A: 100/1=100 (1), 100/3=33.3 (2)
    // B: 20/1=20 (3)
    val result = ElectoralMath.allocateSainteLague(votes, totalSeats)
    result("A") shouldBe 2
    result("B") shouldBe 1
  }

  "Gallagher Index" should "return 0 for perfect proportionality" in {
    val shares = Map("A" -> 0.5, "B" -> 0.5)
    ElectoralMath.calculateGallagherIndex(shares, shares) shouldBe 0.0
  }
}
