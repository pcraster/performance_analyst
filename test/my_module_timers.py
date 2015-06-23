import math
# import random
# import time
from performance_analyst import timer_case


class MyModuleTimers(timer_case.TimerCase):

    # def _moreOrLess(self,
    #        value):
    #   return random.gauss(value, 0.25)

    # def _sleepSomeSeconds(self,
    #        nrSeconds):
    #   time.sleep(self._moreOrLess(nrSeconds))

    def time_c(self):
        # self._sleepSomeSeconds(3.0)
        for i in range(300000):
            math.sqrt(i)

    def time_b(self):
        # self._sleepSomeSeconds(1.0)
        for i in range(100000):
            math.sqrt(i)

    def time_a(self):
        for i in range(200000):
            math.sqrt(i)

    def timeRaiseException(self):
        assert False

    time_a.repeat = 2
    time_b.repeat = 3
    time_c.description = "Superduper fix"
