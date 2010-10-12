import math
# import random
# import time

from PerformanceAnalyst import TimerCase



class MyModuleTimers(TimerCase.TimerCase):

  # def _moreOrLess(self,
  #        value):
  #   return random.gauss(value, 0.25)

  # def _sleepSomeSeconds(self,
  #        nrSeconds):
  #   time.sleep(self._moreOrLess(nrSeconds))

  def timeC(self):
    # self._sleepSomeSeconds(3.0)
    for i in range(300000):
      math.sqrt(i)

  def timeB(self):
    # self._sleepSomeSeconds(1.0)
    for i in range(100000):
      math.sqrt(i)

  def timeA(self):
    for i in range(200000):
      math.sqrt(i)

  def timeRaiseException(self):
    assert False

  timeA.repeat = 2
  timeB.repeat = 3
  timeC.description = "Superduper fix"

