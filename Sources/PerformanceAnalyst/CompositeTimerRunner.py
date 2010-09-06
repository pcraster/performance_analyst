"""
********************
CompositeTimerRunner
********************
"""
import TimerRunner



class CompositeTimerRunner(TimerRunner.TimerRunner, list):
  """
  Instances of this class can contain multiple TimerRunner instances
  and will forward all calls to them.

  This is an implementation of the composite pattern. Using this class you can
  create timer runners (leaves in the pattern's lingo) that, for example,
  write their results to a database *and* will print status information
  to a stream. Without this class that is not possible, since
  :class:`PerformanceAnalyst.SQLiteTimerRunner.SQLiteTimerRunner` class
  instances don't print status information to a stream, and
  :class:`PerformanceAnalyst.StreamTimerRunner.StreamTimerRunner` class
  instances don't write results to a database.

  This class is implemented in terms of a list, so you can use the list's
  interface to manage the leave TimerCase instances.

  See also http://en.wikipedia.org/wiki/Composite_pattern

  .. highlight:: python

  ::

    sqliteRunner = pa.SQLiteTimerRunner.SQLiteTimerRunner(
      databaseName="MyDatabase.sqlite3")
    textRunner = pa.StreamTimerRunner.StreamTimerRunner(stream=sys.stdout)
    compositeRunner = pa.CompositeTimerRunner.CompositeTimerRunner(
      [sqliteRunner, textRunner])

    compositeRunner.run(...)
  """

  def __init__(self,
    iterable):
    TimerRunner.TimerRunner.__init__(self)
    list.__init__(self, iterable)

  def setUp(self,
    nrTimerCases):
    map(lambda leaf: leaf.setUp(nrTimerCases), self)

  def tearDown(self):
    map(lambda leaf: leaf.tearDown(), self)

  def processTimerResult(self,
    result):
    map(lambda leaf: leaf.processTimerResult(result), self)

