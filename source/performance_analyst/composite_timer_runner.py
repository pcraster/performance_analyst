"""
********************
CompositeTimerRunner
********************
"""
import timer_runner


class CompositeTimerRunner(timer_runner.TimerRunner, list):
    """
    Instances of this class can contain multiple TimerRunner instances
    and will forward all calls to them.

    This is an implementation of the composite pattern. Using this class you can
    create timer runners (`leaves` in the pattern's lingo) that, for example,
    write their results to a database *and* will print status information
    to a stream. Without this class that is not possible, since
    :class:`performance_analyst.SQLiteTimerRunner.SQLiteTimerRunner` class
    instances don't print status information to a stream, and
    :class:`performance_analyst.StreamTimerRunner.StreamTimerRunner` class
    instances don't write results to a database.

    This class is implemented in terms of a list, so you can use the list's
    interface to manage the leave TimerCase instances.

    See also http://en.wikipedia.org/wiki/Composite_pattern

    .. highlight:: python

    ::

      sqlite_runner = pa.SQLiteTimerRunner.SQLiteTimerRunner(
          database_name="my_database.sqlite3")
      text_runner = pa.StreamTimerRunner.StreamTimerRunner(stream=sys.stdout)
      composite_runner = pa.CompositeTimerRunner.CompositeTimerRunner(
          [sqlite_runner, text_runner])

      composite_runner.run(...)
    """

    def __init__(self,
            iterable):
        timer_runner.TimerRunner.__init__(self)
        list.__init__(self, iterable)

    def set_up(self,
            nr_timer_cases):
        map(lambda leaf: leaf.set_up(nr_timer_cases), self)

    def tear_down(self):
        map(lambda leaf: leaf.tear_down(), self)

    def process_timer_result(self,
        result):
        map(lambda leaf: leaf.process_timer_result(result), self)
