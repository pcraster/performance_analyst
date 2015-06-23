import unittest
from performance_analyst import timer_runner, timer_suite
import my_module_timers


class TimerRunnerTests(unittest.TestCase):

    def test001(self):
        """Test running the example timer case"""
        runner = timer_runner.TimerRunner()

        # Use suite with list of timers. ---------------------------------------
        result = runner.run(timer_suite.TimerSuite([
            my_module_timers.MyModuleTimers("time_a"),
            my_module_timers.MyModuleTimers("time_b"),
            my_module_timers.MyModuleTimers("time_c"),
        ]))

        self.assertEqual(len(result), 3)
        self.assert_("MyModuleTimers.time_a" in result)
        self.assert_("MyModuleTimers.time_b" in result)
        self.assert_("MyModuleTimers.time_c" in result)

        # Use suite with suite with list of timers. ----------------------------
        result = runner.run(timer_suite.TimerSuite([timer_suite.TimerSuite([
            my_module_timers.MyModuleTimers("time_a"),
            my_module_timers.MyModuleTimers("time_b"),
            my_module_timers.MyModuleTimers("time_c"),
        ])]))

        self.assertEqual(len(result), 3)
        self.assert_("MyModuleTimers.time_a" in result)
        self.assert_("MyModuleTimers.time_b" in result)
        self.assert_("MyModuleTimers.time_c" in result)

        # Use suite with list with timer cases and suite with list with cases. -
        result = runner.run(timer_suite.TimerSuite([
            my_module_timers.MyModuleTimers("time_a"),
            timer_suite.TimerSuite([
                my_module_timers.MyModuleTimers("time_b"),
                my_module_timers.MyModuleTimers("time_c"),
            ])
        ]))

        self.assertEqual(len(result), 3)
        self.assert_("MyModuleTimers.time_a" in result)
        self.assert_("MyModuleTimers.time_b" in result)
        self.assert_("MyModuleTimers.time_c" in result)
