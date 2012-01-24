version            := 0.0.9
pythonVersion      := ${shell python -c 'import sys; print "{0}.{1}".format(*sys.version_info[:2])'}
virtualPythonDir   := bla
virtualPythonBinDir := ${shell python -c 'import sys; print "${virtualPythonDir}/" + ("Scripts" if sys.platform == "win32" else "bin")'}

all: docs tests

doc docs:
	make -C Documentation clean html

test tests:
	make -C Tests all

# Open all files containing the version number.
bumpVersion:
	vi Makefile setup.py Documentation/conf.py Documentation/History.rst Sources/PerformanceAnalyst/_Configuration.py

# Create PerformanceAnalyst-<version>.{tar.gz,zip}
sdist: setup.py
	python setup.py --quiet sdist --formats=gztar,zip

dist: docs sdist
	cd Documentation/_build && zip --quiet --recurse-paths ../../dist/PerformanceAnalyst-${version}-doc.zip html
	ls -ltr dist/PerformanceAnalyst-${version}*

# Install the package in a sandbox and import it.
test_dist: dist
	rm -fr ${virtualPythonDir}
	virtualenv --no-site-packages --quiet ${virtualPythonDir}
	make sdist
	${virtualPythonBinDir}/pip install --quiet psutil
	${virtualPythonBinDir}/pip install --no-index --find-links=file://`pwd`/dist PerformanceAnalyst==${version}
	@echo "*******************************************************************"
	@echo "* Installation succeeded if the next command prints a Python list *"
	@echo "*******************************************************************"
	${virtualPythonBinDir}/python -c "import PerformanceAnalyst; print dir(PerformanceAnalyst)"

clean:
	make -C Sources $@
	make -C Tests $@
	rm -fr ${virtualPythonDir}
	find Sources -name "*.pyc" | xargs --no-run-if-empty rm -f

