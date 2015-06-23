import logging
import sys
import unittest



sys.path = ["../source"] + sys.path

logging.basicConfig(
  level=logging.DEBUG,
  filename="UnitTests.log",
  filemode="w",
)

loader = unittest.defaultTestLoader

if __name__ == "__main__":
  unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
    loader.loadTestsFromName("ImportTests.ImportTests"),
    loader.loadTestsFromName("TimerLoaderTests.TimerLoaderTests"),
    loader.loadTestsFromName("TimerSuiteTests.TimerSuiteTests"),
    loader.loadTestsFromName("TimerRunnerTests.TimerRunnerTests"),
    loader.loadTestsFromName("SQLiteTimerRunnerTests.SQLiteTimerRunnerTests"),
    loader.loadTestsFromName(
      "ProgressTimerRunnerTests.ProgressTimerRunnerTests"),
    loader.loadTestsFromName(
      "CompositeTimerRunnerTests.CompositeTimerRunnerTests"),
  ]))
