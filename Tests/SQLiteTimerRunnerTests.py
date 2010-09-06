import os.path
import sqlite3
import unittest

import PerformanceAnalyst as pa

import MyModuleTimers



class SQLiteTimerRunnerTests(unittest.TestCase):

  def test001(self):
    """Test running the example timer case"""
    databaseName = "TestTimings.sqlite"
    runner = pa.SQLiteTimerRunner.SQLiteTimerRunner(databaseName=databaseName)
    result = runner.run(pa.TimerSuite.TimerSuite([
         MyModuleTimers.MyModuleTimers("timeA"),
         MyModuleTimers.MyModuleTimers("timeB"),
         MyModuleTimers.MyModuleTimers("timeC"),
    ]))

    self.assertEqual(len(result), 3)
    self.assert_("MyModuleTimers.timeA" in result)
    self.assert_("MyModuleTimers.timeB" in result)
    self.assert_("MyModuleTimers.timeC" in result)

    self.assert_(os.path.isfile(databaseName))
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    tableNames = [
         "MyModuleTimers_timeA",
         "MyModuleTimers_timeB",
         "MyModuleTimers_timeC"
    ]

    for tableName in tableNames:
      # Check existence of tables in data base.
      self.assert_(not cursor.execute(
         "pragma table_info(%s)" % (tableName)).fetchone() is None)

      # Check format of tables.
      # TODO

      # Check contents of tables.
      # TODO

    records = cursor.execute("select * from MyModuleTimers_timeA").fetchall()
    self.assertEqual(len(records), 2)
    records = cursor.execute("select * from MyModuleTimers_timeB").fetchall()
    self.assertEqual(len(records), 3)
    records = cursor.execute("select * from MyModuleTimers_timeC").fetchall()
    self.assertEqual(len(records), 1)

    connection.close()
    self.assert_(os.path.isfile(databaseName))
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    # Make sure we can run the timers again using the same database.
    result = runner.run(pa.TimerSuite.TimerSuite([pa.TimerSuite.TimerSuite([
         MyModuleTimers.MyModuleTimers("timeA"),
         MyModuleTimers.MyModuleTimers("timeB"),
         MyModuleTimers.MyModuleTimers("timeC"),
    ])]))

    # Test that tables have grown.
    records = cursor.execute("select * from MyModuleTimers_timeA").fetchall()
    self.assertEqual(len(records), 4)
    records = cursor.execute("select * from MyModuleTimers_timeB").fetchall()
    self.assertEqual(len(records), 6)
    records = cursor.execute("select * from MyModuleTimers_timeC").fetchall()
    self.assertEqual(len(records), 2)

