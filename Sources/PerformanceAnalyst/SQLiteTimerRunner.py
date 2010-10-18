"""
*****************
SQLiteTimerRunner
*****************

.. Warning::

   * This is work in progress, so don't forget to create backups of your timings database file. Bugs in the software can easely render the database file useless. Since the whole database is stored in a single file, just copying the file to a safe location suffices.
   * Once in a while a new version of the software may require a database structure change (new tables, new fields, etc). The PerformanceAnalyst tries to hide this fact as much as possible. Database updates will happen behind the scenes, when an old database is used by a new version of the software for the first time. This may take a long time to complete, depending on the size of the database and the exact changes that need to be made. Do not interupt this process!
"""
import sqlite3

import _Configuration
import datetime
import TimerRunner



class SQLiteTimerRunner(TimerRunner.TimerRunner):

  @classmethod
  def version(cls,
    cursor):
    """
    Return the version of the software that updated the database the last time.

    An integer value is returned.
    """
    record = cursor.execute(
      "SELECT version FROM History ORDER BY version DESC").fetchone()
    return record[0]

  @classmethod
  def _initializeTimingTable(cls,
    cursor,
    name):
    cursor.execute("""CREATE TABLE %s (
      timestamp TEXT,
      real_time REAL,
      cpu_time REAL)""" % (name))
      # real_time REAL CONSTRAINT DEFAULT 0.0)""" % (tableName))

  @classmethod
  def _initializeHistoryTable(cls,
    cursor):
    # History table doesn't exist already.
    # Create it and put in a dummy version number that's lower than the one
    # that introduced the history table.
    assert cursor.execute("PRAGMA TABLE_INFO(History)").fetchone() is None
    assert _Configuration.versionAsInteger() >= 5

    cursor.execute("""CREATE TABLE History (
      timestamp TEXT,
      version INTEGER,
      description TEXT)""")
    timeStamp = datetime.datetime.utcnow().isoformat(" ")
    version = 5 # 0.0.5
    description = "Initialized History table"
    tuple_ = (timeStamp, version, description)
    cursor.execute(
      "INSERT INTO History VALUES (\"{0}\", {1}, \"{2}\")".format(*tuple_))

  @classmethod
  def updateDatabase(cls,
    connection,
    cursor):
    """
    Do everything necessary to bring the database up to date with the current version of the software.

    Once in a while a new version of the software may require a database structure change (new tables, new fields, etc). This function should be called before other parts of the software start using the database file.
    """
    # The database layout depends on the version of the Performance Analyst
    # that has been used to update the database last. This information is
    # stored in the a table called 'History'. This table has the folowing
    # layout:
    #
    # | date | version | description |
    #
    # With these fields:
    # date       : Date the run started.
    # version    : Version of Performance Analyst used in run.
    # description: Description of why the database changed.

    # The History table was added to the database after the first versions of
    # the Performance Analyst where already released.
    if cursor.execute("PRAGMA TABLE_INFO(History)").fetchone() is None:
      cls._initializeHistoryTable(cursor)

    assert not cursor.execute("PRAGMA TABLE_INFO(History)").fetchone() is None
    databaseVersion = cls.version(cursor)

    assert databaseVersion <= _Configuration.versionAsInteger(), \
      "Database created with newer version of the software. Update software."

    # Database changes, by version:
    # 0.0.6:
    # - Renamed field duration to cpu_time
    # - Added field real_time

    if databaseVersion < 6:
      # For each table containing timings:
      # - Rename the table to some tmp name.
      # - Create new currentVersion of the table.
      # - Copy original data from tmp table to new table. Insert dummy value
      #   for new fields.
      # - Remove tmp table.
      for record in cursor.execute("SELECT * FROM sqlite_master").fetchall():
        tableName = record[1]

        if tableName.find("_time") != -1:
          tmpTableName = "{0}_tmp".format(tableName)
          cursor.execute("ALTER TABLE {0} RENAME TO {1}".format(
            tableName, tmpTableName))
          cls._initializeTimingTable(cursor, tableName)
          # Use cpu_time for real_time too. We don't have anything better right
          # now.
          cursor.execute("""INSERT INTO {0}(timestamp, real_time, cpu_time)
            SELECT timestamp, duration, duration
            FROM {1}""".format(tableName, tmpTableName))
          cursor.execute("DROP TABLE {0}".format(tmpTableName))

      # Add info to the history table.
      timeStamp = datetime.datetime.utcnow().isoformat(" ")
      version = 6 # 0.0.6
      description = "Renamed field duration to cpu_time. Added field real_time."
      tuple_ = (timeStamp, version, description)
      cursor.execute(
        "INSERT INTO History VALUES (\"{0}\", {1}, \"{2}\")".format(*tuple_))

    # if databaseVersion < 7:
    #   ...

    connection.commit()

    assert cls.version(cursor) == _Configuration.versionAsInteger()

  def __init__(self,
    databaseName): # ="Timings"):
    """
    `databaseName`
      Name of sqlite3 database to write results to.
    """
    assert not databaseName is None

    TimerRunner.TimerRunner.__init__(self)
    self.databaseName = databaseName

  def setUp(self,
    nrTimerCases):
    self.connection = sqlite3.connect(self.databaseName)
    self.cursor = self.connection.cursor()
    self.updateDatabase(self.connection, self.cursor)

  def tearDown(self):
    # Otherwise data might not be written!
    self.connection.commit()

    self.cursor.close()
    self.connection.close()

    self.cursor = None
    self.connection = None

  def processTimerResult(self,
    result):
    key = result.keys()[0]
    tableName = key.replace(".", "_")

    if self.cursor.execute("PRAGMA TABLE_INFO(%s)" % (tableName)).fetchone() \
      is None:
      self._initializeTimingTable(self.cursor, tableName)

    timeStamp = result[key][0].isoformat(" ")
    # description = result[key][1]

    for timings in result[key][2]:
      # timings is a tuple of (real_time, cpu_time).
      tuple_ = (timeStamp, timings[0], timings[1])
      self.cursor.execute("INSERT INTO %s VALUES (?, ?, ?)" % (tableName),
        tuple_)

  def databaseIsConsistent(self):
    """
    Test the integrity of the database.

    This function should always return True. If not, the database may be
    corrupt.
    """
    connection = sqlite3.connect(self.databaseName)
    cursor = connection.cursor()

    # All tables must be non-empty.
    for masterTableRecord in cursor.execute(
      "select * from sqlite_master").fetchall():
      tableName = masterTableRecord[1]

      if tableName.find("time") != -1:
        tableRecord = cursor.execute(
          "select * from {0}".format(tableName)).fetchone()
        if tableRecord is None:
          return False

    # Passed all tests.
    return True

