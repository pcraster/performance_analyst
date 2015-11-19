"""
*********
TimerCase
*********
"""
import datetime
import inspect
import os
import psutil


def time_delta_in_seconds(
      delta):
  return (delta.microseconds +
      (delta.seconds + delta.days * 24.0 * 3600.0) * 10.0**6) / 10.0**6


class TimerCase(object):
    """
    Timer case instances are the things that get timed by the framework.

    A :class:`timer runner <performance_analyst.timer_runner.TimerRunner>`
    can be used to time a collection of :class:`timer suites
    <performance_analyst.timer_suite.TimerSuite>` containing
    timer cases.
    """

    @classmethod
    def set_up_class(cls):
        """
        Perform initial actions needed by the timer suite.

        The default does nothing. Override when necessary.
        """
        pass

    @classmethod
    def tear_down_class(cls):
        """
        Perform clean-up needed by the timer suite.

        The default does nothing. Override when necessary.
        """
        pass

    @classmethod
    def add_method(cls,
            method):
        """
        Binds the `method` passed in to the class.

        This is a convenience function to use when adding time methods to
        timer cases programmatically at runtime.
        """
        setattr(cls, method.__name__, method)

    def __init__(self,
            method_name):
        """
        Construct a TimerCase.

        :param str method_name: Name of the sub-class' member function to time.

        Construction of timer cases is done by the :class:`timer loader
        <performance_analyst.TimerLoader.TimerLoader>`. You normally
        don't need to call the constructor yourself.
        """
        self.method_name = method_name
        self.method = inspect.getmembers(self, lambda object: \
            inspect.ismethod(object) and \
            object.__name__ == self.method_name)[0][1]

    def set_up(self):
        """
        Perform initial actions needed by the timer case.

        The default does nothing. Override when necessary.
        """
        pass

    def tear_down(self):
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
        return u"{}.{}".format(self.method.__self__.__class__.__name__,
            self.method_name)

    def run(self,
            result):
        """
        Run the timer case, storing the results in `result`.

        This function takes care of calling :meth:`set_up`, the layered
        method, and :meth:`tear_down`, at the appropriate times.
        """
        self.set_up()

        timings = []
        process = psutil.Process(os.getpid())

        for i in range(getattr(self.method, "repeat", 1)):
            user_cpu_time, system_cpu_time = process.cpu_times()
            start_real_time = datetime.datetime.now()
            start_cpu_time = user_cpu_time + system_cpu_time

            self.method()

            user_cpu_time, system_cpu_time = process.cpu_times()
            end_real_time = datetime.datetime.now()
            end_cpu_time = user_cpu_time + system_cpu_time

            real_time_duration_in_seconds = time_delta_in_seconds(
                end_real_time - start_real_time)
            cpu_time_duration_in_seconds = end_cpu_time - start_cpu_time

            timings.append((real_time_duration_in_seconds,
                cpu_time_duration_in_seconds))

        self.tear_down()

        result[self.id()] = [datetime.datetime.now(),
            unicode(getattr(self.method, "description", self.id())), timings]

    def nr_timer_cases(self):
        return 1
