import logging
import sys
import unittest


sys.path = ["../source"] + sys.path

logging.basicConfig(
  level=logging.DEBUG,
  filename="unit_tests.log",
  filemode="w",
)

loader = unittest.defaultTestLoader

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
        loader.loadTestsFromName("import_tests.ImportTests"),
        loader.loadTestsFromName("timer_loader_tests.TimerLoaderTests"),
        loader.loadTestsFromName("timer_suite_tests.TimerSuiteTests"),
        loader.loadTestsFromName("timer_runner_tests.TimerRunnerTests"),
        loader.loadTestsFromName(
            "sqlite_timer_runner_tests.SQLiteTimerRunnerTests"),
        loader.loadTestsFromName(
            "progress_timer_runner_tests.ProgressTimerRunnerTests"),
        loader.loadTestsFromName(
            "composite_timer_runner_tests.CompositeTimerRunnerTests"),
    ]))
