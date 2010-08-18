import datetime
import unittest

from PerformanceAnalyst import TimerResult, TimerSuite

import MyModuleTimers



class TimerSuiteTests(unittest.TestCase):

  def test001(self):
    """Test running an example timer suite"""
    suite = TimerSuite.TimerSuite([
         MyModuleTimers.MyModuleTimers("timeA"),
         MyModuleTimers.MyModuleTimers("timeB"),
         MyModuleTimers.MyModuleTimers("timeC"),
    ])
    self.assertEqual(len(suite), 3)
    self.assertEqual(suite[0].id(), "MyModuleTimers.timeA")
    self.assertEqual(suite[1].id(), "MyModuleTimers.timeB")
    self.assertEqual(suite[2].id(), "MyModuleTimers.timeC")

    result = TimerResult.TimerResult()
    suite.run(result)

    self.assertEqual(len(result), 3)

    # timeA --------------------------------------------------------------------
    self.assertEqual(len(result[suite[0].id()]), 3)
    self.assertEqual(len(result[suite[0].id()][2]), 2)

    # Time stamp.
    timeStamp = result[suite[0].id()][0]
    today = datetime.date.today()

    self.assert_(isinstance(timeStamp, datetime.datetime), timeStamp)
    self.assertEqual(timeStamp.year, today.year)
    self.assertEqual(timeStamp.month, today.month)
    self.assertEqual(timeStamp.day, today.day)

    # Description.
    description = result[suite[0].id()][1]
    self.assert_(isinstance(description, unicode))
    self.assertEqual(description, suite[0].id())

    # Durations.
    durations = result[suite[0].id()][2]
    self.assertEqual(len(durations), 2)

    for duration in durations:
      self.assert_(isinstance(duration, float))
      self.assert_(duration > 0.0)

    # timeB --------------------------------------------------------------------
    self.assertEqual(len(result[suite[1].id()]), 3)
    self.assertEqual(len(result[suite[1].id()][2]), 3)

    # timeC --------------------------------------------------------------------
    self.assertEqual(len(result[suite[2].id()]), 3)
    self.assertEqual(len(result[suite[2].id()][2]), 1)

    description = result[suite[2].id()][1]
    self.assert_(isinstance(description, unicode))
    self.assertEqual(description, u"Superduper fix")

