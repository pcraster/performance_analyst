"""
***********
TimerRunner
***********
"""
import timer_result
import timer_case
import timer_suite


class TimerRunner(object):
    """
    A timer runner instance manages the execution of a timer suite with
    timer cases.

    This default implementation just executes the timer cases passed into
    the run method and has no side effects. Specialized implementations
    can do additional things, like printing status messages, writing
    results to a database, send an email, cook a meal, whatever.
    """

    def set_up(self,
            nr_timer_cases):
        """
        Perform initial actions needed by the timer runner.

        :param int nr_timer_cases: Number of timer cases in the suites
            to be run.

        This function is called by :meth:`run`. The default does nothing.
        Override when necessary.
        """
        pass

    def tear_down(self):
        """
        Perform clean-up needed by the timer runner.

        This function is called by :meth:`run`. The default does nothing.
        Override when necessary.
        """
        pass

    def process_timer_result(self,
             result):
        """
        Perform some side effect based on the timer result obtained by running a
        timer case.

        This function is called after running each timer case in turn.

        This function is called by :meth:`run`. The default does nothing.
        Override when necessary.
        """
        pass

    def run_timer_case(self,
            case):
        # From unittest's docs:
        # A test case is the smallest unit of testing. It checks for a specific
        # response to a particular set of inputs. unittest provides a base
        # class, TestCase, which may be used to create new test cases.
        assert isinstance(case, timer_case.TimerCase)

        result = timer_result.TimerResult()

        case.run(result)
        assert len(result) == 1
        self.process_timer_result(result)

        return result

    def run_timer_suite(self,
            suite):
        # From unittest's docs:
        # A test suite is a collection of test cases, test suites, or both. It
        # is used to aggregate tests that should be executed together.
        assert isinstance(suite, timer_suite.TimerSuite)

        # For this suite no cases have been running yet.
        self.current_timer_case_class.append(None)

        result = timer_result.TimerResult()

        for item in suite:
            assert isinstance(item, (timer_suite.TimerSuite,
                timer_case.TimerCase))

            if isinstance(item, timer_suite.TimerSuite):
                result.update(self.run_timer_suite(item))
            elif isinstance(item, timer_case.TimerCase):
                # Each timer case class' set_up_class() must be called
                # before the first timer case is run.
                # Each timer case class' tear_down_class must be called
                # after the last timer case has run.
                if self.current_timer_case_class[-1] is None:
                    self.current_timer_case_class[-1] = item.__class__
                    self.current_timer_case_class[-1].set_up_class()
                elif self.current_timer_case_class[-1] != item.__class__:
                    self.current_timer_case_class[-1].tear_down_class()
                    self.current_timer_case_class[-1] = item.__class__
                    self.current_timer_case_class[-1].set_up_class()

                case_result = self.run_timer_case(item)
                result.update(case_result)

        assert len(self.current_timer_case_class) > 0
        if self.current_timer_case_class[-1] is not None:
            self.current_timer_case_class[-1].tear_down_class()

        self.current_timer_case_class.pop()

        return result

    def run(self,
            suite):
        """
        Run all timer cases found in `suite`.

        This function calls :meth:`set_up`, :meth:`process_timer_result`, and
        :meth:`tear_down` at the appropriate times.
        """
        self.current_timer_case_class = []
        self.set_up(suite.nr_timer_cases())

        result = self.run_timer_suite(suite)

        self.tear_down()
        self.current_timer_case_class = []

        return result
