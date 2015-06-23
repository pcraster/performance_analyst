SHELL    := bash

first: all
all: tests

tests: clean
	python tests.py

plot plots:
	pa.py plot TestTimings.pdf TestTimings.sqlite MyModuleTimers_timeA MyModuleTimers_timeB MyModuleTimers_timeC

clean:
	rm -f *.pyc unit_tests.log
	rm -f MyDataBase.sql3
	rm -f TestTimings.{sqlite,pdf}
