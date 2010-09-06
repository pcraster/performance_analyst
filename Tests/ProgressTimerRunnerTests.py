import StringIO
import unittest

import PerformanceAnalyst as pa

import MyModuleTimers



class ProgressTimerRunnerTests(unittest.TestCase):

  def test001(self):
    """Test running the example timer case"""
    stream = StringIO.StringIO()
    runner = pa.ProgressTimerRunner.ProgressTimerRunner(stream=stream)
    result = runner.run(pa.TimerSuite.TimerSuite([
      MyModuleTimers.MyModuleTimers("timeA"),
      MyModuleTimers.MyModuleTimers("timeB"),
      MyModuleTimers.MyModuleTimers("timeC"),
    ]))

    # Test stream contents.
    self.assertEqual(stream.getvalue(), """\
1/3 finished
2/3 finished
3/3 finished
""")

