"""
***********
TimerRunner
***********
"""
import TimerResult
import TimerCase
import TimerSuite



class TimerRunner(object):
  """
  A timer runner instance manages the execution of a timer suite with timer
  cases.

  This default implementation just executes the timer cases passed into the
  run method and has no side effects. Specialized implementations can do
  additional things, like printing status messages, writing results to a
  database, send an email, cook a meal, whatever.
  """

  def setUp(self,
    nrTimerCases):
    """
    Perform initial actions needed by the timer runner.

    `nrTimerCases`
      Number of timer cases in the suites to be run.

    This function is called by :meth:`run`. The default does nothing.
    Override when necessary.
    """
    pass

  def tearDown(self):
    """
    Perform clean-up needed by the timer runner.

    This function is called by :meth:`run`. The default does nothing.
    Override when necessary.
    """
    pass

  def processTimerResult(self,
         result):
    """
    Perform some side effect based on the timer result obtained by running a
    timer case.

    This function is called after running each timer case in turn.

    This function is called by :meth:`run`. The default does nothing.
    Override when necessary.
    """
    pass

  def _runTimerCase(self,
         case):
    # From unittest's docs:
    # A test case is the smallest unit of testing. It checks for a specific
    # response to a particular set of inputs. unittest provides a base
    # class, TestCase, which may be used to create new test cases.
    assert isinstance(case, TimerCase.TimerCase)

    result = TimerResult.TimerResult()

    case.run(result)
    assert len(result) == 1
    self.processTimerResult(result)

    return result

  def _runTestSuite(self,
         suite):
    # From unittest's docs:
    # A test suite is a collection of test cases, test suites, or both. It
    # is used to aggregate tests that should be executed together.
    assert isinstance(suite, TimerSuite.TimerSuite)

    result = TimerResult.TimerResult()

    for item in suite:
      assert isinstance(item, (TimerSuite.TimerSuite, TimerCase.TimerCase))

      if isinstance(item, TimerSuite.TimerSuite):
        result.update(self._runTestSuite(item))
      elif isinstance(item, TimerCase.TimerCase):
        caseResult = self._runTimerCase(item)
        result.update(caseResult)

    return result

  def run(self,
         suite):
    """
    Run all timer cases found in `suite`.

    This function calls :meth:`setUp`, :meth:`processTimerResult`, and
    :meth:`tearDown` at the appropriate times.
    """
    self.setUp(suite.nrTimerCases())

    result = self._runTestSuite(suite)

    self.tearDown()

    return result

