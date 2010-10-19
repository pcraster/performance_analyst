.. _history:

*******
History
*******

0.0.7 (in development)
======================
-

0.0.6
=====
- Added SQLiteTimerRunner.databaseIsConsistent.
- Added support for tracking real time, besides CPU-time. This required a change in the database structure. See the :py:mod:`SQLiteTimerRunner's warnings <PerformanceAnalyst.SQLiteTimerRunner>`!
- The `pa.py ls` command now orders the per-timer results by timestamp.
- The `pa.py plot` command not has a `timestamp` option which is used to select timestamps to use for plot. Data created before this timestamp is skipped.

0.0.5
=====
- Added TimerLoader.loadTimersFromTimerCase.
- Fixed bug in documentation generation.
- On Windows, installation of the PerformanceAnalyst won't install psutil and matplotlib anymore, since that doesn't work. The user has to install the requirements separately.

0.0.4
=====
- Removed bug in TextTimerRunner.
- Renamed TextTimerRunner into StreamTimerRunner.
- Added CompositeTimerRunner, ProgressTimerRunner.
- Updated license from GPL to MIT. Do whatever you want with this software, commercially or not.

0.0.3
=====
- The egg file now installs pa.py in the Scripts/bin directory of the Python installation.

0.0.2
=====
- Added lots of documentation.

0.0.1
=====
- Initial release.

