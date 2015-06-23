"""
*******************
ProgressTimerRunner
*******************
"""
import sys
import timer_runner


class ProgressTimerRunner(timer_runner.TimerRunner):
    """
    Timer runner that prints progress to a stream.

    This runner class can be used in case you want to keep track of
    the progress of running timer cases.
    """

    def __init__(self,
            stream=sys.stdout):
        """
        :param file stream: Stream to write progress to.
        """
        timer_runner.TimerRunner.__init__(self)
        self.stream = stream

    def set_up(self,
            nr_timer_cases):
        self.nr_timer_cases = nr_timer_cases
        self.current_timer_case = 0

    def process_timer_result(self,
            result):
        self.current_timer_case += 1
        self.stream.write("{}/{} finished\n".format(self.current_timer_case,
            self.nr_timer_cases))
        self.stream.flush()
