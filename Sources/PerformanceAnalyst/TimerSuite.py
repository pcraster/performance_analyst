"""
**********
TimerSuite
**********
"""



class TimerSuite(list):
  """
  A timer suite is a list of timer cases, timer suites, or both.

  It is used to aggregate timers that should be executed together.
  """

  def __init__(self,
         timers):
    """
    Construct a timer suite.

    `timers`
      Collection of timer cases, timer suites, or both.
    """
    list.__init__(self, timers)

  def run(self,
         result):
    """
    Runs all timer cases contained in the suite.

    Results are stored in the `result` object passed in.
    """
    for timer in self:
      timer.run(result)

