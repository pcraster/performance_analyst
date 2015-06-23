"""
*****************
StreamTimerRunner
*****************
"""
import sys

import TimerRunner



class StreamTimerRunner(TimerRunner.TimerRunner):
  """
  Timer runner that prints results to a stream.

  This runner class can be used if the results of running the timer cases does
  not need to be persisted, for example in case of doing some test runs with
  timer cases.
  """

  def __init__(self,
         stream=sys.stdout):
    """
    `stream`
      Stream to write results to.
    """
    TimerRunner.TimerRunner.__init__(self)
    self.stream = stream

  def processTimerResult(self,
         result):
    self.stream.write(str(result))
    self.stream.flush()

