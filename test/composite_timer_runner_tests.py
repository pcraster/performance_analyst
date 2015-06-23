import os.path
import sqlite3
import StringIO
import unittest
import performance_analyst as pa
import my_module_timers


class CompositeTimerRunnerTests(unittest.TestCase):

  def _init(self):
      self.database_name = "CompositeTimerRunnerTests.sqlite"
      if os.path.isfile(self.database_name):
          os.remove(self.database_name)

  def setUp(self):
      self._init()

  def tearDown(self):
      self._init()

  def test001(self):
      """Test running the example timer case"""
      sqlite_runner = pa.sqlite_timer_runner.SQLiteTimerRunner(
          database_name=self.database_name)
      stream = StringIO.StringIO()
      stream_runner = pa.stream_timer_runner.StreamTimerRunner(stream=stream)
      runner = pa.composite_timer_runner.CompositeTimerRunner([sqlite_runner,
          stream_runner])

      # Make sure the database doesn't exist yet.
      self.assert_(not os.path.isfile(self.database_name))

      result = runner.run(pa.timer_suite.TimerSuite([
          my_module_timers.MyModuleTimers("time_a"),
          my_module_timers.MyModuleTimers("time_b"),
          my_module_timers.MyModuleTimers("time_c"),
      ]))

      # Make sure the database got created.
      self.assert_(os.path.isfile(self.database_name))

      # Test stream contents.
      self.assert_("MyModuleTimers.time_a" in stream.getvalue())
