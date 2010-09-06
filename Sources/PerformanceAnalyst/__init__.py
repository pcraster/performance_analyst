"""
******************
PerformanceAnalyst
******************
This package is for timing pieces of code and keeping track of the timings over time for postprocessing. The design and terminology is based on Python's `unit testing framework <http://docs.python.org/library/unittest.html#module-unittest>`_, so it may be useful to refer to its documentation too.
"""

import CompositeTimerRunner
import ProgressTimerRunner
import SQLiteTimerRunner
import StreamTimerRunner
import TimerCase
import TimerLoader
import TimerResult
import TimerRunner
import TimerSuite

