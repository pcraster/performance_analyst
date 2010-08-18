"""
*****************
SQLiteTimerRunner
*****************
"""
import sqlite3

import TimerRunner



class SQLiteTimerRunner(TimerRunner.TimerRunner):

  def __init__(self,
         databaseName): # ="Timings"):
    """
    `databaseName`
      Name of sqlite3 database to write results to.
    """
    assert not databaseName is None

    TimerRunner.TimerRunner.__init__(self)
    self.databaseName = databaseName

  def _initialiseTimingTable(self,
         tableName):
    self.cursor.execute("""create table %s (
         timestamp text,
         duration REAL)""" % (tableName))
         # description text,

  def setUp(self):
    self.connection = sqlite3.connect(self.databaseName)
    self.cursor = self.connection.cursor()

  def tearDown(self):
    # Otherwise data might not be written!
    self.connection.commit()

    self.cursor.close()
    self.connection.close()

    self.cursor = None
    self.connection = None

  def processTimerResult(self,
         result):
    # Open sqlite table
    key = result.keys()[0]
    tableName = key.replace(".", "_")

    if self.cursor.execute("pragma table_info(%s)" % (tableName)).fetchone() \
         is None:
      self._initialiseTimingTable(tableName)

    timeStamp = result[key][0].isoformat(" ")
    # description = result[key][1]
    timings = result[key][2]

    for timing in timings:
      tuple_ = (timeStamp, timing)
      self.cursor.execute("insert into %s values (?, ?)" % (tableName), tuple_)

