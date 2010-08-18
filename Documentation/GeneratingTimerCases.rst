**********************
Generating timer cases
**********************

For every timer case a member function must be implemented with the Python code to time.

.. highlight:: python

::

  from PerformanceAnalyst import TimerCase

  class MyModuleTimings(TimerCase.TimerCase):

    def timeA(self):
      # Statements to time.
      pass

    def timeB(self):
      # Other statements to time.
      pass

If in this example :meth:`timeA` and :meth:`timeB` are very similar, and there are more of these similar timer case member functions, then they should be generated at runtime. Given Python's dynamic nature, this is not a difficult thing to accomplish.

The idea is to add member functions to a :class:`TimerCase` sub-class at runtime. The implementation of each of these memberfunctions consists of a section of boilerplate statements of which the details are filled in at runtime. The :class:`TimerCase` base class contains a :meth:`convenience function<PerformanceAnalyst.TimerCase.TimerCase.addMethod>` to add methods to it programmatically.

In the next example this idea is used in a very silly use-case. These few lines of code do create 1000 timer cases though! Now you can focus on the method's boilerplate implementation instead of copy-paste-adjusting 1000 member functions.

.. highlight:: python

::

  class MyModuleTimings(TimerCase.TimerCase):

    # Empty class, but there could also be handcrafted functions here.
    pass

  def _createMethod(count):

    def method(self):
      math.sqrt(count)  # Very silly example.

    # Format a unique name (within the timer case).
    method.__name__ = "timeSqrt_%d" % (count)

    return method

  for count in xrange(1000):
    MyModuleTimings.addMethod(_createMethod(count))
