"""
*********
TimerCase
*********
"""
import datetime
import inspect
import os
import psutil



class TimerCase(object):
  """
  Timer case instances are the things that get timed by the framework.

  A :class:`timer runner <PerformanceAnalyst.TimerRunner.TimerRunner>` can be
  used to time a collection of
  :class:`timer suites <PerformanceAnalyst.TimerSuite.TimerSuite>` containing
  timer cases.
  """

  @classmethod
  def addMethod(cls,
         method):
    """
    Binds the `method` passed in to the class.

    This is a convenience function to use when adding time methods to
    timer cases programmatically at runtime.
    """
    setattr(cls, method.__name__, method)

  def __init__(self,
         methodName):
    """
    Construct a TimerCase.

    `methodName`
      Name of the sub-class' member function to time.

    Construction of timer cases is done by the
    :class:`timer loader <PerformanceAnalyst.TimerLoader.TimerLoader>`. You
    normally don't need to call the constructor yourself.
    """
    self.methodName = methodName
    self.method = inspect.getmembers(self, lambda object: \
         inspect.ismethod(object) and \
         object.__name__ == self.methodName)[0][1]

  def setUp(self):
    """
    Perform initial actions needed by the timer case.

    The default does nothing. Override when necessary.
    """
    pass

  def tearDown(self):
    """
    Perform clean-up needed by the timer case.

    The default does nothing. Override when necessary.
    """
    pass

  def id(self):
    """
    Return the id of the timer case.

    The id is a string with a unique value. It is formatted as folows::

      <timer case class name>.<timer case method name>
    """
    return u"%s.%s" % (self.method.__self__.__class__.__name__, self.methodName)

  def run(self,
         result):
    """
    Run the timer case, storing the results in `result`.

    This function takes care of calling :meth:`setUp`, the layered method, and
    :meth:`tearDown`, at the appropriate times.
    """
    self.setUp()

    timings = []
    process = psutil.Process(os.getpid())

    for i in range(getattr(self.method, "repeat", 1)):
      userTime, systemTime = process.get_cpu_times()
      startTime = userTime + systemTime

      self.method()

      userTime, systemTime = process.get_cpu_times()
      endTime = userTime + systemTime

      timings.append(endTime - startTime)

    self.tearDown()

    result[self.id()] = [datetime.datetime.now(),
         unicode(getattr(self.method, "description", self.id())), timings]

