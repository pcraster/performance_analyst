import unittest

from PerformanceAnalyst import TimerLoader



class TimerLoaderTests(unittest.TestCase):

  def test001(self):
    """Test detection of individual timer cases in timer suite"""
    loader = TimerLoader.TimerLoader()
    suite = loader.loadTimersFromName("MyModuleTimers.MyModuleTimers")
    self.assertEqual(len(suite), 4)
    self.assertEqual(suite[0].id(), "MyModuleTimers.timeA")
    self.assertEqual(suite[1].id(), "MyModuleTimers.timeB")
    self.assertEqual(suite[2].id(), "MyModuleTimers.timeC")
    self.assertEqual(suite[3].id(), "MyModuleTimers.timeRaiseException")

