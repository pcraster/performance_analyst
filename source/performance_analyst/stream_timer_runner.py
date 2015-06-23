"""
*****************
StreamTimerRunner
*****************
"""
import sys
import timer_runner


class StreamTimerRunner(timer_runner.TimerRunner):
    """
    Timer runner that prints results to a stream.

    This runner class can be used if the results of running the timer
    cases does not need to be persisted, for example in case of doing
    some test runs with timer cases.
    """

    def __init__(self,
            stream=sys.stdout):
        """
        :param file stream: Stream to write results to.
        """
        timer_runner.TimerRunner.__init__(self)
        self.stream = stream

    def process_timer_result(self,
            result):
        self.stream.write(str(result))
        self.stream.flush()
