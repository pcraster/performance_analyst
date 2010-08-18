***********
Quick start
***********

Below is a small example of a Python module which uses a timer loader to run a collection of timer cases aggregated in timer suites.

.. highlight:: python

::

  import PerformanceAnalyst as pa

  loader = pa.TimerLoader.TimerLoader()

  pa.SQLiteTimerRunner.SQLiteTimerRunner(
         databaseName="MyDatabase.sqlite3").run(pa.TimerSuite.TimerSuite([
    loader.loadTimerFromName("MyModuleTimings.MyModuleTimings"),
    # ... More timer suites ...
  ]))

In this case, timer cases are read from the Python module `MyModuleTimings.py`. To simulate a real world example, the sleep function is used to spend some time doing nothing.

.. highlight:: python

::

  import random
  import time

  from PerformanceAnalyst import TimerCase

  class MyModuleTimings(TimerCase.TimerCase):

    def setUp(self):
      pass

    def tearDown(self):
      pass

    def _moreOrLess(self,
           value):
      return random.gauss(value, 0.25)

    def _sleepSomeSeconds(self,
           nrSeconds):
      time.sleep(self._moreOrLess(nrSeconds))

    def timeC(self):
      self._sleepSomeSeconds(3.0)

    def timeB(self):
      self._sleepSomeSeconds(1.0)

    def timeA(self):
      self._sleepSomeSeconds(2.0)

    # Repeat the timings for some timer cases more than once.
    timeA.repeat = 2
    timeB.repeat = 3

    # Use this description instead of the default.
    timeC.description = "Superduper fix"
