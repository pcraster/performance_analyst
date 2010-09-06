import os.path
import sqlite3
import StringIO
import unittest

import PerformanceAnalyst as pa

import MyModuleTimers



class CompositeTimerRunnerTests(unittest.TestCase):

  def _init(self):
    self.databaseName = "CompositeTimerRunnerTests.sqlite"
    if os.path.isfile(self.databaseName):
      os.remove(self.databaseName)

  def setUp(self):
    self._init()

  def tearDown(self):
    self._init()

  def test001(self):
    """Test running the example timer case"""
    sqliteRunner = pa.SQLiteTimerRunner.SQLiteTimerRunner(
      databaseName=self.databaseName)
    stream = StringIO.StringIO()
    streamRunner = pa.StreamTimerRunner.StreamTimerRunner(
      stream=stream)
    runner = pa.CompositeTimerRunner.CompositeTimerRunner([sqliteRunner,
      streamRunner])

    # Make sure the database doesn't exist yet.
    self.assert_(not os.path.isfile(self.databaseName))

    result = runner.run(pa.TimerSuite.TimerSuite([
      MyModuleTimers.MyModuleTimers("timeA"),
      MyModuleTimers.MyModuleTimers("timeB"),
      MyModuleTimers.MyModuleTimers("timeC"),
    ]))

    # Make sure the database got created.
    self.assert_(os.path.isfile(self.databaseName))

    # Test stream contents.
    self.assert_("MyModuleTimers.timeA" in stream.getvalue())

