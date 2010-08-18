"""
***********
TimerLoader
***********
"""
import imp
import inspect

import TimerSuite



class TimerLoader(object):
  """
  Timer loaders create timer cases based on the timer case sub-classes found in
  a module.
  """

  def loadTimersFromName(self,
         name):
    """
    Load timer cases from a module with a :class:`PerformanceAnalyst.TimerCase.TimerCase` sub-class.

    `name`
      Name of module, formatted as `<module>.<TimerCase sub-class>`.

    The `name` passed in is split by the dot to obtain the name of the module
    and the name of the TimerCase sub-class.

    The sub-class is inspected for member functions that have a `time` prefix.
    Each of these is used to fill a timer suite with TimerCase sub-class
    instances.

    So, in case the TimerCase sub-class has three member functions, named
    `timeA`, `timeB` and `timeC`, than this method creates a
    :class:`timer suite <PerformanceAnalyst.TimerSuite.TimerSuite>` containing
    three TimerCase sub-class instances.
    """
    names = name.split(".")
    assert len(names) == 2, "Use <module>.<TimerCase sub-class>"
    moduleName = names[0]
    className = names[1]

    fileDescriptor, pathName, description = imp.find_module(moduleName)

    with fileDescriptor:
      module = imp.load_module(moduleName, fileDescriptor, pathName,
         description)

    class_ = [tuple[1] for tuple in \
         inspect.getmembers(module, inspect.isclass) \
         if tuple[0] == className][0]
    methodNames = [tuple[0] for tuple in \
         inspect.getmembers(class_, inspect.ismethod) \
         if tuple[0].find("time") == 0]

    return TimerSuite.TimerSuite([class_(methodName) \
         for methodName in methodNames])

  def loadTimersFromNames(self,
         names):
    """
    Load timer cases from a number of modules.

    `names`
      Iterable with names of TimerCase sub-classes.
    """
    return [self.loadTimersFromName(name) for name in names]

