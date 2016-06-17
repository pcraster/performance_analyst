# Performance Analyst
The Performance Analyst is a Python package for timing snippets of Python
code. The results can be stored in a database and postprocessed using a
command line tool. This is useful for tracking the performance of Python
software over time. A [tool called pa.py](documentation/pa.md) is supplied
which can be used to query and manage the database contents and to create
plots of the performance results.

The performance is measured by the amount of
[wall clock time](http://en.wikipedia.org/wiki/Wall_clock_time) and
[CPU time](http://en.wikipedia.org/wiki/CPU_time>) in seconds.

The software is modelled after the
[Python unit test library](http://docs.python.org/library/unittest.html#module-unittest),
which makes it easy to use if you are familiar with that. The terminology
is similar to the terms used in the unit test library:

term         | Description
------------ | -----------------------------------------------------------------
timer case   | A method which contains the code that needs to be timed
timer suite  | A class in which related time cases are aggregated
timer loader | Loads timer suites and their associated timer cases
timer runner | Executes all test cases and handles the results, like storing them in a database


Further info:
- [Installation](INSTALL.md)
- [Quick start](documentation/quick_start.md)
- [Generating timer cases](documentation/generating_timer_cases.md)
- [Changes](CHANGES.md)
