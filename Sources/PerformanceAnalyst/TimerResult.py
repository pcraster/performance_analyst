"""
***********
TimerResult
***********
"""



class TimerResult(dict):
  """
  Dictionary with the results of running timer cases.

  The key of the dictionary is the :meth:`id of the timer cases
  <PerformanceAnalyst.TimerCase.TimerCase.id>`.

  The value that is stored for each key is a list with the folowing items::

    [<time stamp>, <description | id>, [<timings>]]

  The first item is the time stamp of the moment the timer case finished. The
  second item is the description or the
  :meth:`timer case's id <PerformanceAnalyst.TimerCase.TimerCase.id>` if no
  description was found. The third item is a list of timings, one for
  each time the timer case was run. Timings are in seconds.
  """

  def __str__(self):
    """
    Return string representation of the results.

    For each timer case the result is formatted as folows::

      <key>
      <time stamp> <description | id> <timing1>
      <time stamp> <description | id> <timing2>
      ...
    """
    result = []

    for key in self:
      result.append(key)

      for timing in self[key][2]:
        result.append("%s %s %g" % (str(self[key][0]), self[key][1], timing))

    return "\n".join(result) + "\n"
