import unittest

from PerformanceAnalyst import TimerRunner, TimerSuite

import MyModuleTimers



class TimerRunnerTests(unittest.TestCase):

  def test001(self):
    """Test running the example timer case"""
    runner = TimerRunner.TimerRunner()

    # Use suite with list of timers. -------------------------------------------
    result = runner.run(TimerSuite.TimerSuite([
      MyModuleTimers.MyModuleTimers("timeA"),
      MyModuleTimers.MyModuleTimers("timeB"),
      MyModuleTimers.MyModuleTimers("timeC"),
    ]))

    self.assertEqual(len(result), 3)
    self.assert_("MyModuleTimers.timeA" in result)
    self.assert_("MyModuleTimers.timeB" in result)
    self.assert_("MyModuleTimers.timeC" in result)

    # Use suite with suite with list of timers. --------------------------------
    result = runner.run(TimerSuite.TimerSuite([TimerSuite.TimerSuite([
         MyModuleTimers.MyModuleTimers("timeA"),
         MyModuleTimers.MyModuleTimers("timeB"),
         MyModuleTimers.MyModuleTimers("timeC"),
    ])]))

    self.assertEqual(len(result), 3)
    self.assert_("MyModuleTimers.timeA" in result)
    self.assert_("MyModuleTimers.timeB" in result)
    self.assert_("MyModuleTimers.timeC" in result)

    # Use suite with list with timer cases and suite with list with cases. -----
    result = runner.run(TimerSuite.TimerSuite([
         MyModuleTimers.MyModuleTimers("timeA"),
         TimerSuite.TimerSuite([
           MyModuleTimers.MyModuleTimers("timeB"),
           MyModuleTimers.MyModuleTimers("timeC"),
         ])
    ]))

    self.assertEqual(len(result), 3)
    self.assert_("MyModuleTimers.timeA" in result)
    self.assert_("MyModuleTimers.timeB" in result)
    self.assert_("MyModuleTimers.timeC" in result)

