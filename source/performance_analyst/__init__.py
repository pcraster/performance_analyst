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

from configuration import *

import composite_timer_runner
import progress_timer_runner
import sqlite_timer_runner
import stream_timer_runner
import timer_case
import timer_loader
import timer_result
import timer_runner
import timer_suite
