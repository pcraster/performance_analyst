# Quick start
Below is a small example of a Python module which uses a *timer loader*
to run a collection of *timer cases* aggregated in *timer suites*. A *timer runner* is used to collect the timings into a database.


```python
import performance_analyst as pa

loader = pa.TimerLoader()

pa.SQLiteTimerRunner(
        database_name="my_database.sqlite3").run(
    loader.load_timers_from_name("my_module_timings.MyModuleTimings"),
    # ... More timer suites ...
)
```


In this case, timer cases are read from the Python module
`my_module_timings.py`. To simulate a real world example, the sleep
function is used to spend some time doing nothing.


```python
import random
import time
from performance_analyst import TimerCase


class MyModuleTimings(TimerCase):

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def more_or_less(self,
            value):
        return random.gauss(value, 0.25)

    def sleep_some_seconds(self,
            nr_seconds):
        time.sleep(self.more_or_less(nr_seconds))

    def time_c(self):
        self.sleep_some_seconds(3.0)

    def time_b(self):
        self.sleep_some_seconds(1.0)

    def time_a(self):
        self.sleep_some_seconds(2.0)


# Repeat the timings for some timer cases more than once.
time_a.repeat = 2
time_b.repeat = 3

# Use this description instead of the default.
time_c.description = "Superduper fix"
```
