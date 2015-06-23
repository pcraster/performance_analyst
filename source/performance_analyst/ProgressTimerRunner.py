"""
*******************
ProgressTimerRunner
*******************
"""
import sys

import TimerRunner



class ProgressTimerRunner(TimerRunner.TimerRunner):
  """
  Timer runner that prints progress to a stream.

  This runner class can be used in case you want to keep track of the progress
  of running timer cases.
  """

  def __init__(self,
    stream=sys.stdout):
    """
    `stream`
      Stream to write progress to.
    """
    TimerRunner.TimerRunner.__init__(self)
    self.stream = stream

  def setUp(self,
    nrTimerCases):
    self.nrTimerCases = nrTimerCases
    self.currentTimerCase = 0

  def processTimerResult(self,
    result):
    self.currentTimerCase += 1
    self.stream.write("%d/%d finished\n" % (self.currentTimerCase,
      self.nrTimerCases))
    self.stream.flush()

