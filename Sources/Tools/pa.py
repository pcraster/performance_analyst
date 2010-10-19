#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. _pa.py:

*****
pa.py
*****
PerformanceAnalyst commandline utility. The PerformanceAnalyst packages stores information in a database. This command can be used to query and manage this database and to create plots of the performance results.

The commandline syntax is similar to tools like `svn <http://subversion.tigris.org>`_ and `git <http://git-scm.com>`_. The command uses multiple sub-commands with their own set of commandline options.

Type:

.. highlight:: bash

::

  pa.py --help

or:

.. highlight:: bash

::

  pa.py help

for the general commandline usage.

Type:

.. highlight:: bash

::

  pa.py help <command>

or:

.. highlight:: bash

::

  pa.py <command> --help

For the commandline usage of a sub-command.

Here is an example that creates a pdf with a plot with three graphs:

.. highlight:: bash

::

  pa.py plot TestTimings.pdf TestTimings.sqlite MyModuleTimers_timeA MyModuleTimers_timeB MyModuleTimers_timeC

Now follows a short rundown of the usage of the sub-commands of the pa.py command. Check the tool's usage for further details.

The high-level usage of the pa.py command is as folows::

  pa.py [options] <command>

Command is one of the sub-commands:

**ls**
  List the contents of the performance database::

    pa.py ls [options] <database> {timer}+

  **database**
    Name of performance database.

  **timer**
    Name of timer.
**mv**
  Move (rename) timers stored in the performance database::

    pa.py mv [options] <database> <current timer> <new timer>

  **database**
    Name of performance database.

  **current timer**
    Current name of timer.

  **new timer**
    New name of timer.
**plot**
  Plot timers stored in the performance database::

    pa.py plot [options] <output> <database> <timer>+

  The plot will contain two lines for each timer: a solid line for the cpu-time
  and a dashed line for the real-time.

  **output**
    Name of output pdf.

  **database**
    Name of performance database.

  **timer**
    Name of timer.
**rm**
  Remove timers stored in the performance database::

    pa.py rm [options] <database> <timer>+

  **database**
    Name of performance database.

  **timer**
    Name of timer.
**stat**
  Calculate statistics of timers stored in the performance database::

    pa.py stat [options] <database> <timer>+

  **database**
    Name of performance database.

  **timer**
    Name of timer.
**history**
  Print history of the database::

    pa.py stat [options] <database>

  **database**
    Name of performance database.
"""

import datetime
from optparse import OptionParser
import os.path
import re
import sqlite3
import sys

import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import numpy
import pylab

from PerformanceAnalyst import SQLiteTimerRunner



def _uniquefyList(list_):
  """
  Remove duplicates from `list_` and retain the order of the items.

  The first occurrence of an item is retained. Subsequent items with the same
  value are deleted.

  A new list with the resulting items is returned.
  """
  seen = set()
  return [item for item in  list_ if item not in seen and not seen.add(item)]



def _stringToTimestamp(
  string):
  try:
    # String with microseconds.
    timestamp = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")
  except ValueError:
    # String without microseconds.
    timestamp = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

  return timestamp



class _OptionParser(OptionParser):
  def format_epilog(self,
         formatter):
    return "\n%s\n" % (self.epilog.strip())



class _Command(object):

  def __init__(self,
         arguments,
         usage,
         epilog=""):
    self.arguments = arguments
    self.parser = _OptionParser(usage=usage, epilog=epilog)
    self.databaseName = None

  def printHelp(self):
    self.parser.print_help()

  def _addTimestampOption(self):
    self.parser.add_option("--timestamp",
         dest="timestamp",
         default="latest",
         help="timestamp to select (timestamp, 'latest' or -1, -2, -3, etc)")

  def _timestamps(self,
         cursor,
         name):
    records = cursor.execute(
         "select timestamp from %s order by timestamp" % (name)).fetchall()
    assert len(records) > 0, "No records found for %s" % (name)

    # Remove duplicates and sort result.
    records = list(set([record[0] for record in records]))
    records.sort()

    return records

  def _timestampByIndex(self,
         cursor,
         name,
         offset):
    result = None
    timestamps = self._timestamps(cursor, name)

    if len(timestamps) >= abs(offset):
      result = timestamps[offset]

    return result

  def _parseTimestamps(self,
         cursor,
         names,
         timestamps):
    symbols = timestamps.split(":")
    timestamps = [[] for _ in range(len(names))]

    for symbol in symbols:
      for i in range(len(names)):
        if symbol == "latest":
          timestamp = self._timestampByIndex(cursor, names[i], -1)

          if not timestamp is None:
            timestamps[i].append(timestamp)
        elif re.match("-\d+", symbol):
          timestamp = self._timestampByIndex(cursor, names[i], int(symbol) - 1)

          if not timestamp is None:
            timestamps[i].append(timestamp)
        else:
          timestamps[i].append(symbol)

    assert len(timestamps) == len(names)

    return timestamps

  def _timerNames(self,
         cursor):
    return [record[1] for record in \
         cursor.execute("select * from sqlite_master").fetchall()]

  def _parseTimerNames(self,
         cursor,
         patterns):
    """Determine which timer names match the regular expressions in `patterns`.

    The patterns in `patterns` are used as regular expressions. The rules for
    matching regular expressions is different from shell expansion rules. Use
    the `ls` sub-command of `pa.py` to test your expressions patterns before
    issueing the `rm` sub-command, for example.
    """
    result = []
    timerNames = self._timerNames(cursor)

    for pattern in patterns:
      pattern = re.compile("^%s$" % (pattern))
      for timerName in timerNames:
        if pattern.match(timerName):
          result.append(timerName)

    return _uniquefyList(result)


  def _updateDatabase(self,
    connection,
    cursor):
    # The runner knows best whether the database must be updated and how to
    # do it.
    SQLiteTimerRunner.SQLiteTimerRunner.updateDatabase(connection, cursor)



class _Plot(_Command):

  def __init__(self,
         arguments=[]):
    _Command.__init__(self, arguments,
         usage="Usage: plot [options] <output> <database> <timer>+",
         epilog= """
Creates a pdf with a plot of all timers supplied.
""")

  def parseArguments(self):
    (options, arguments) = self.parser.parse_args(self.arguments)

    if len(arguments) < 3:
      self.printHelp()
      sys.exit(2)

    self.outputFileName = arguments[0]
    self.databaseName = arguments[1]
    self.names = arguments[2:]

  def _aggregateData(self,
         data,
         algorithm):
    algorithms = {
      "min": numpy.nanmin,
      "mean": numpy.mean,
      "std": numpy.std,
    }

    return algorithms[algorithm](data)

  def _readData(self,
    cursor,
    tableName):
    assert not cursor.execute(
      "PRAGMA TABLE_INFO(%s)" % (tableName)).fetchone() is None, \
        "Table %s does not exist" % (tableName)

    realTimes = {}
    cpuTimes = {}

    for record in cursor.execute("select * from %s" % (tableName)).fetchall():
      timestamp = _stringToTimestamp(record[0])

      # CPU-time is in the third field. Skip real-time for now.
      realTime = float(record[1])
      cpuTime = float(record[2])

      if not timestamp in realTimes:
        assert not timestamp in cpuTimes
        realTimes[timestamp] = [realTime]
        cpuTimes[timestamp] = [cpuTime]
      else:
        assert timestamp in cpuTimes
        realTimes[timestamp].append(realTime)
        cpuTimes[timestamp].append(cpuTime)

    for timestamp in realTimes:
      realTimes[timestamp] = numpy.array(realTimes[timestamp])
      cpuTimes[timestamp] = numpy.array(cpuTimes[timestamp])

    return realTimes, cpuTimes

  def run(self):
    self.parseArguments()

    assert os.path.isfile(self.databaseName), "Database %s does not exist" % (
      self.databaseName)

    connection = sqlite3.connect(self.databaseName)
    cursor = connection.cursor()
    self._updateDatabase(connection, cursor)

    figure = pyplot.figure(figsize=(15, 10))
    axis = figure.add_subplot(111)
    realTimes, realTimesMean, realTimesStd = {}, {}, {}
    cpuTimes, cpuTimesMean, cpuTimesStd = {}, {}, {}

    for name in self.names:
      # Tuples of (real_time, cpu_time)
      realTimes[name], cpuTimes[name] = self._readData(cursor, name)

    lines = {}

    # Calculate statistics.
    for name in self.names:
      realTimesMean[name] = [self._aggregateData(realTimes[name][timestamp],
         algorithm="mean") for timestamp in sorted(realTimes[name])]
      cpuTimesMean[name] = [self._aggregateData(cpuTimes[name][timestamp],
         algorithm="mean") for timestamp in sorted(cpuTimes[name])]
      realTimesStd[name] = [self._aggregateData(realTimes[name][timestamp],
         algorithm="std") for timestamp in sorted(realTimes[name])]
      cpuTimesStd[name] = [self._aggregateData(cpuTimes[name][timestamp],
         algorithm="std") for timestamp in sorted(cpuTimes[name])]

    # Plot mean timing.
    for name in self.names:
      # Store properties of plot with real-time values.
      lines[name] = axis.plot(sorted(realTimes[name]), realTimesMean[name],
        "o-")[0]
      axis.plot(sorted(cpuTimes[name]), cpuTimesMean[name], "o--",
        color=lines[name].get_color())

    # Plot error bars.
    for name in self.names:
      axis.errorbar(sorted(realTimes[name]), realTimesMean[name],
        realTimesStd[name], fmt="o", color=lines[name].get_color())
      axis.errorbar(sorted(cpuTimes[name]), cpuTimesMean[name],
        cpuTimesStd[name], fmt="o", color=lines[name].get_color())

    legend = pyplot.figlegend([lines[name] for name in self.names], self.names,
      "upper right") # loc=(0.0, 0.0))

    for text in legend.get_texts():
      text.set_fontsize("small")

    axis.set_title(self.databaseName)
    axis.set_xlabel("Timestamps")
    axis.set_ylabel("Time (s)")
    limits = axis.get_xlim()
    axis.set_xlim(limits[0] - 0.1, limits[1] + 0.1)
    axis.grid(True)

    figure.autofmt_xdate()

    pylab.savefig(self.outputFileName)

    return 0



class _Ls(_Command):

  def __init__(self,
         arguments=[]):
    _Command.__init__(self, arguments,
         usage="Usage: ls [options] <database> {timer}+",
         epilog="""
Lists all timers if no timer is provided. Shows some details if one or more
timers are provided.
""")

  def parseArguments(self):
    (options, arguments) = self.parser.parse_args(self.arguments)

    if len(arguments) < 1:
      self.printHelp()
      sys.exit(2)

    self.databaseName = arguments[0]
    self.names = arguments[1:]

  def run(self):
    self.parseArguments()

    assert os.path.isfile(self.databaseName), \
         "Database %s does not exist" % (self.databaseName)

    connection = sqlite3.connect(self.databaseName)
    cursor = connection.cursor()
    self._updateDatabase(connection, cursor)

    if len(self.names) == 0:
      for record in cursor.execute("select * from sqlite_master").fetchall():
        sys.stdout.write("%s\n" % (record[1]))
    else:
      self.names = self._parseTimerNames(cursor, self.names)

      for name in self.names:
        records = cursor.execute("select * from %s" % (name)).fetchall()
        timestamps = {}

        for record in records:
          if not record[0] in timestamps:
            timestamps[record[0]]  = 1
          else:
            timestamps[record[0]] += 1

        if len(timestamps) > 0:
          sys.stdout.write("%s\n" % (name))

        for timestamp in timestamps:
          sys.stdout.write("%s\t%d\n" % (timestamp, timestamps[timestamp]))

    return 0



class _Mv(_Command):

  def __init__(self,
         arguments=[]):
    _Command.__init__(self, arguments,
         usage="Usage: mv [options] <database> <current timer> <new timer>",
         epilog="""
Rename a timer case.
""")

  def parseArguments(self):
    (options, arguments) = self.parser.parse_args(self.arguments)

    if len(arguments) != 3:
      self.printHelp()
      sys.exit(2)

    self.databaseName = arguments[0]
    self.names = arguments[1:]

  def run(self):
    self.parseArguments()

    assert os.path.isfile(self.databaseName), \
         "Database %s does not exist" % (self.databaseName)

    connection = sqlite3.connect(self.databaseName)
    cursor = connection.cursor()
    self._updateDatabase(connection, cursor)

    assert len(self.names) == 2

    cursor.execute("alter table %s rename to %s" % (self.names[0],
      self.names[1]))
    connection.commit()

    return 0



class _Rm(_Command):

  def __init__(self,
         arguments=[]):
    _Command.__init__(self, arguments,
         usage="Usage: rm [options] <database> <timer>+",
         epilog="""
Remove a timer case from the database.
""")
    self._addTimestampOption()

  def parseArguments(self):
    (options, arguments) = self.parser.parse_args(self.arguments)

    if len(arguments) < 2:
      self.printHelp()
      sys.exit(2)

    self.timestamps = options.timestamp
    self.databaseName = arguments[0]
    self.names = arguments[1:]

  def run(self):
    self.parseArguments()

    assert os.path.isfile(self.databaseName), \
         "Database %s does not exist" % (self.databaseName)

    connection = sqlite3.connect(self.databaseName)
    cursor = connection.cursor()
    self._updateDatabase(connection, cursor)

    self.names = self._parseTimerNames(cursor, self.names)
    self.timestamps = self._parseTimestamps(cursor, self.names, self.timestamps)

    for i in xrange(len(self.names)):
      for timestamp in self.timestamps[i]:
        tuple_ = (timestamp,)
        cursor.execute("delete from %s where timestamp=?" % (self.names[i]),
              tuple_)

    # Remove whole table:
    # cursor.execute("drop table %s" % (self.names[i]))

    connection.commit()

    return 0



class _Stat(_Command):

  def __init__(self,
         arguments=[]):
    _Command.__init__(self, arguments,
         usage="Usage: stat [options] <database> <timer>+",
         epilog="""
%s

Queries the database and calculates some statistics for the timings passed in:

  summary
    Print some summary statistics (min, max, mean, etc).

  quotient
    Print quotient of timings. If the name of one timer case is passed, than a
    temporal quotient is calculated: the quotient of the last and previous
    timing of the timer case.
    If more than one timer case is passed, than quotients are calculated
    between the first timer case and all subsequent timer cases.

  timing
    Print the timing of each timer case, as found in the database. Nothing is
    calculated in this case.
""" % ("Statistic types are: %s" % ("|".join(["summary", "quotient", "timing"]))))
    # self.parser.add_option("--summary",
    #      help="print summary statistics")
    self._addTimestampOption()
    self.parser.add_option("--type",
         dest="type",
         choices=["summary", "quotient", "timing"],
         default="summary",
         help="calculate some statistic (%default)")

  def parseArguments(self):
    (options, arguments) = self.parser.parse_args(self.arguments)

    if len(arguments) < 2:
      self.printHelp()
      sys.exit(2)

    self.timestamps = options.timestamp
    self.type = options.type
    self.databaseName = arguments[0]
    self.names = arguments[1:]

  def _indexOfTimestamp(self,
         cursor,
         name,
         timestamp):
    return self._timestamps(cursor, name).index(timestamp)

  def _timings(self,
         cursor,
         name,
         timestamp):
    tuple_ = (timestamp,)
    records = cursor.execute("SELECT cpu_time FROM %s WHERE timestamp=?" % (
         name), tuple_).fetchall()
    return [record[0] for record in records]

  def _writeSummaryStatistics(self,
         cursor):
    for i in range(len(self.names)):
      assert len(self.timestamps[i]) == 1
      timings = self._timings(cursor, self.names[i], self.timestamps[i][0])
      assert len(timings) > 0

      mean = numpy.mean(timings, dtype=numpy.float64)
      std = numpy.std(timings, dtype=numpy.float64)
      cv = std / mean

      sys.stdout.write("%s (%s):\n" % (self.names[i], self.timestamps[i]))
      sys.stdout.write("min : %g\n" % (numpy.min(timings)))
      sys.stdout.write("max : %g\n" % (numpy.max(timings)))
      sys.stdout.write("mean: %g\n" % (mean))
      sys.stdout.write("std : %g\n" % (std))
      sys.stdout.write("cv  : %g\n" % (cv))

  def _writeTemporalQuotient(self,
         cursor):
    assert len(self.names) == 1

    # if len(self.names) == 0:
    #   self.names = [record[1] for record in cursor.execute(
    #      "select * from sqlite_master").fetchall()]

    for i in range(len(self.names)):
      if len(self.timestamps[i]) == 1:
        # Append the previous timestamp.
        index = self._indexOfTimestamp(cursor, self.names[i],
              self.timestamps[i][0]) - 1
        self.timestamps[i].append(self._timestampByIndex(cursor, self.names[i],
              index))

    for i in range(len(self.names)):
      # List of lowest timings for each timestamp.
      min = [numpy.min(self._timings(cursor, self.names[i],
           self.timestamps[i][j])) for j in range(2)]
      assert len(min) == 2
      assert min[1] != 0.0, "%s %s" % (self.names[i], self.timestamps[i])
      quotient = min[0] / min[1]
      sys.stdout.write("%g\n" % (quotient))

  def _writeQuotient2(self,
         cursor):
    assert len(self.names) > 1, "At least two names required for quotient"
    for i in range(len(self.names)):
      assert len(self.timestamps[i]) == 1

    # List of lowest timings for each name in self.names.
    min = [numpy.min(self._timings(cursor, self.names[i],
         self.timestamps[i][0])) for i in range(len(self.names))]

    # List of quotients of first timing and subsequent timings.
    quotients = [min[0] / min[i] for i in range(1, len(self.names))]

    # Write comma-seperated list of quotients.
    sys.stdout.write(", ".join(["%g" % (quotients[i]) for i in \
         range(len(quotients))]))

  def _writeQuotient(self,
         cursor):
    if len(self.names) <= 1:
      self._writeTemporalQuotient(cursor)
    else:
      self._writeQuotient2(cursor)

  def _writeTiming(self,
         cursor):
    assert len(self.names) > 0
    for i in range(len(self.names)):
      assert len(self.timestamps[i]) == 1

    # List of lowest timings for each name in self.names.
    timings = [numpy.min(self._timings(cursor, self.names[i],
         self.timestamps[i][0])) for i in range(len(self.names))]

    # Write comma-seperated list of timings.
    sys.stdout.write("%s\n" % (", ".join(["%g" % (timings[i]) for i in \
         range(len(timings))])))

  def run(self):
    self.parseArguments()

    assert os.path.isfile(self.databaseName), \
         "Database %s does not exist" % (self.databaseName)

    connection = sqlite3.connect(self.databaseName)
    cursor = connection.cursor()
    self._updateDatabase(connection, cursor)

    self.names = self._parseTimerNames(cursor, self.names)
    self.timestamps = self._parseTimestamps(cursor, self.names, self.timestamps)

    if self.type == "summary":
      self._writeSummaryStatistics(cursor)
    elif self.type == "quotient":
      self._writeQuotient(cursor)
    elif self.type == "timing":
      self._writeTiming(cursor)

    return 0



class _History(_Command):

  def __init__(self,
         arguments=[]):
    _Command.__init__(self, arguments,
         usage="Usage: history [options] <database>",
         epilog= """
Print history of the database.
""")

  def parseArguments(self):
    (options, arguments) = self.parser.parse_args(self.arguments)

    if len(arguments) != 1:
      self.printHelp()
      sys.exit(2)

    self.databaseName = arguments[0]

  def run(self):
    self.parseArguments()

    assert os.path.isfile(self.databaseName), \
         "Database %s does not exist" % (self.databaseName)

    connection = sqlite3.connect(self.databaseName)
    cursor = connection.cursor()
    self._updateDatabase(connection, cursor)

    records = cursor.execute(
      "SELECT * FROM History ORDER BY timestamp ASC").fetchall()

    for record in records:
      timestamp = _stringToTimestamp(record[0])
      version = record[1]
      description = record[2]

      sys.stdout.write("{0} {1} {2}\n".format(timestamp, version, description))



if __name__ == "__main__":
  commands = {
    "plot": _Plot,
    "ls": _Ls,
    "mv": _Mv,
    "rm" : _Rm,
    "stat" : _Stat,
    "history" : _History,
  }

  def testCommand(
           command):
    if not command in commands:
      sys.stderr.write("Command not one of '%s'\n" % (", ".join(commands)))
      sys.exit(2)

  usage = "Usage: %prog [options] <command>"
  epilog = """
See 'pa.py help <command>' for more information on a specific command.

Commands are: %s
""" % (" | ".join(commands))

  parser = _OptionParser(usage=usage, epilog=epilog)
  parser.disable_interspersed_args()
  (options, arguments) = parser.parse_args()

  command = None

  if len(arguments) >= 1:
    command = arguments[0]

  if command is None:
    parser.print_help()
    sys.exit(2)
  elif command == "help":
    if len(arguments) < 2:
      parser.print_help()
    else:
      command2 = arguments[1]
      testCommand(command2)
      commands[command2]().printHelp()

    sys.exit(0)

  testCommand(command)
  sys.exit(commands[command](arguments[1:]).run())

