version            := 0.0.9
pythonVersion      := ${shell python -c 'import sys; print "{0}.{1}".format(*sys.version_info[:2])'}
virtualPythonDir   := bla
virtualPythonBinDir := ${shell python -c 'import sys; print "${virtualPythonDir}/" + ("Scripts" if sys.platform == "win32" else "bin")'}

all: docs tests

doc docs:
	make -C documentation clean html

test tests:
	make -C test all

# Open all files containing the version number.
bumpVersion:
	vi Makefile setup.py documentation/conf.py documentation/History.rst source/performance_analyst/_Configuration.py

# Create performance_analyst-<version>.{tar.gz,zip}
sdist: setup.py
	python setup.py --quiet sdist --formats=gztar,zip

dist: docs sdist
	cd documentation/_build && zip --quiet --recurse-paths ../../dist/performance_analyst-${version}-doc.zip html
	ls -ltr dist/performance_analyst-${version}*

# Install the package in a sandbox and import it.
test_dist: dist
	rm -fr ${virtualPythonDir}
	virtualenv --no-site-packages --quiet ${virtualPythonDir}
	make sdist
	${virtualPythonBinDir}/pip install --quiet psutil
	${virtualPythonBinDir}/pip install dist/performance_analyst-${version}.zip
	@echo "*******************************************************************"
	@echo "* Installation succeeded if the next command prints a Python list *"
	@echo "*******************************************************************"
	${virtualPythonBinDir}/python -c "import performance_analyst; print dir(performance_analyst)"

clean:
	make -C source $@
	make -C test $@
	rm -fr ${virtualPythonDir}
	find source -name "*.pyc" | xargs --no-run-if-empty rm -f

