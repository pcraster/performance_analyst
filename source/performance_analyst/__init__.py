"""
*******************
performance_analyst
*******************
This package is for timing pieces of code and keeping track
of the timings over time for postprocessing. The design
and terminology is based on Python's `unit testing framework
<http://docs.python.org/library/unittest.html#module-unittest>`_, so it
may be useful to refer to its documentation too.
"""
from composite_timer_runner import *
from configuration import *
from progress_timer_runner import *
from sqlite_timer_runner import *
from stream_timer_runner import *
from timer_case import *
from timer_loader import *
from timer_result import *
from timer_runner import *
from timer_suite import *
