"""
***********
TimerLoader
***********
"""
import imp
import inspect
import timer_suite


class TimerLoader(object):
    """
    Timer loaders create timer cases based on the timer case sub-classes
    found in a module.
    """

    def load_timers_from_name(self,
            name):
        """
        Load timer cases from a module with a
        :class:`performance_analyst.TimerCase.TimerCase` sub-class.

        :param str name: Name of module, formatted as
            `<module>.<TimerCase sub-class>`.

        The `name` passed in is split by the dot to obtain the name of
        the module and the name of the TimerCase sub-class.

        The sub-class is inspected for member functions that have a
        `time` prefix. Each of these is used to fill a timer suite with
        TimerCase sub-class instances.

        So, in case the TimerCase sub-class has three member functions,
        named `time_a`, `time_b` and `time_c`, than this method creates a
        :class:`timer suite <performance_analyst.timer_suite.TimerSuite>`
        containing three TimerCase sub-class instances.
        """
        names = name.split(".")
        assert len(names) == 2, "Use <module>.<TimerCase sub-class>"
        module_name = names[0]
        class_name = names[1]

        file_descriptor, pathname, description = imp.find_module(module_name)

        with file_descriptor:
            module = imp.load_module(module_name, file_descriptor, pathname,
                description)

        class_ = [tuple[1] for tuple in \
            inspect.getmembers(module, inspect.isclass) if tuple[0] == \
                class_name][0]
        return self.load_timers_from_timer_case(class_)

    def load_timers_from_names(self,
            names):
        """
        Load timer cases from a number of modules.

        :param iterable names: Iterable with names of TimerCase sub-classes.
        """
        return [self.load_timers_from_name(name) for name in names]

    def load_timers_from_timer_case(self,
            class_):
        """
        Load timer cases from a TimerCase derived `class_`.

        :param class class_: TimerCase derived class to load timer
            cases from.
        """
        method_names = [tuple[0] for tuple in \
            inspect.getmembers(class_, inspect.ismethod) \
                if tuple[0].find("time") == 0]

        return timer_suite.TimerSuite([class_(method_name) \
            for method_name in method_names])
