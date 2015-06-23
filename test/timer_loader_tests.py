import unittest
from performance_analyst import timer_loader


class TimerLoaderTests(unittest.TestCase):

    def test001(self):
        """Test detection of individual timer cases in timer suite"""
        loader = timer_loader.TimerLoader()
        suite = loader.load_timers_from_name("my_module_timers.MyModuleTimers")
        self.assertEqual(len(suite), 4)
        self.assertEqual(suite[0].id(), "MyModuleTimers.timeRaiseException")
        self.assertEqual(suite[1].id(), "MyModuleTimers.time_a")
        self.assertEqual(suite[2].id(), "MyModuleTimers.time_b")
        self.assertEqual(suite[3].id(), "MyModuleTimers.time_c")
