import datetime
import unittest
from performance_analyst import TimerResult, TimerSuite
import my_module_timers


class TimerSuiteTests(unittest.TestCase):

    def test001(self):
        """Test running an example timer suite"""
        suite = TimerSuite([
            my_module_timers.MyModuleTimers("time_a"),
            my_module_timers.MyModuleTimers("time_b"),
            my_module_timers.MyModuleTimers("time_c"),
        ])
        self.assertEqual(len(suite), 3)
        self.assertEqual(suite[0].id(), "MyModuleTimers.time_a")
        self.assertEqual(suite[1].id(), "MyModuleTimers.time_b")
        self.assertEqual(suite[2].id(), "MyModuleTimers.time_c")

        result = TimerResult()
        suite.run(result)

        self.assertEqual(len(result), 3)

        # time_a ---------------------------------------------------------------
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
        durationTuples = result[suite[0].id()][2]
        self.assertEqual(len(durationTuples), 2)

        for durationTuple in durationTuples:
            self.assert_(isinstance(durationTuple, tuple))
            self.assertEqual(len(durationTuples), 2)
            for duration in durationTuple:
                self.assert_(isinstance(duration, float))
                self.assert_(duration > 0.0)

        # time_b ---------------------------------------------------------------
        self.assertEqual(len(result[suite[1].id()]), 3)
        self.assertEqual(len(result[suite[1].id()][2]), 3)

        # time_c ---------------------------------------------------------------
        self.assertEqual(len(result[suite[2].id()]), 3)
        self.assertEqual(len(result[suite[2].id()][2]), 1)

        description = result[suite[2].id()][1]
        self.assert_(isinstance(description, unicode))
        self.assertEqual(description, u"Superduper fix")
