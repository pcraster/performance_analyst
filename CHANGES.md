# Changes

## 0.0.10
- Added support for class level fixtures (set_up_class, tear_down_class).

## 0.0.9
- Updated code to conform to PEP8.
- Minor refactorings. Renamed files, reorganized files, updated documentation,
  ...
- Moved project from SourceForge to GitHub.

## 0.0.8
- The package is now distributed as a source distribution that can be installed and uninstalled using pip. See the [Installation page](INSTALL.md) for more information.

## 0.0.7
- The `pa.py stat` command now also prints the real-time timings into account. The format of the output is changed a bit.

## 0.0.6
- Added SQLiteTimerRunner.databaseIsConsistent.
- Added support for tracking real time, besides CPU-time. This required a change in the database structure. See the SQLiteTimerRunner's warnings (`performance_analyst.SQLiteTimerRunner`)!
- The `pa.py ls` command now orders the per-timer results by timestamp.
- The `pa.py plot` command not has a `timestamp` option which is used to select timestamps to use for plot. Data created before this timestamp is skipped.

## 0.0.5
- Added TimerLoader.loadTimersFromTimerCase.
- Fixed bug in documentation generation.
- On Windows, installation of the Performance Analyst won't install psutil and matplotlib anymore, since that doesn't work. The user has to install the requirements separately.

## 0.0.4
- Removed bug in TextTimerRunner.
- Renamed TextTimerRunner into StreamTimerRunner.
- Added CompositeTimerRunner, ProgressTimerRunner.
- Updated license from GPL to MIT. Do whatever you want with this software, commercially or not.

## 0.0.3
- The egg file now installs pa.py in the Scripts/bin directory of the Python installation.

## 0.0.2
- Added lots of documentation.

## 0.0.1
- Initial release.
