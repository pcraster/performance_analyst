import StringIO
import unittest
import performance_analyst as pa
import my_module_timers


class ProgressTimerRunnerTests(unittest.TestCase):

    def test001(self):
      """Test running the example timer case"""
      stream = StringIO.StringIO()
      runner = pa.progress_timer_runner.ProgressTimerRunner(stream=stream)
      result = runner.run(pa.timer_suite.TimerSuite([
          my_module_timers.MyModuleTimers("time_a"),
          my_module_timers.MyModuleTimers("time_b"),
          my_module_timers.MyModuleTimers("time_c"),
      ]))

      # Test stream contents.
      self.assertEqual(stream.getvalue(), """\
1/3 finished
2/3 finished
3/3 finished
""")
