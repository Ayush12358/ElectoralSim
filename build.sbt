name := "ElectoralSimulation"
version := "0.1.0"
scalaVersion := "2.13.12"

libraryDependencies ++= Seq(
  "org.apache.commons" % "commons-math3" % "3.6.1",
  "com.typesafe" % "config" % "1.4.2",
  "org.scalatest" %% "scalatest" % "3.2.17" % Test
)

// Placeholder for BharatSim repository if external
// resolvers += "BharatSim Repo" at "https://..."
