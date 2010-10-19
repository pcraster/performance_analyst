version            := 0.0.7
pythonVersion      := ${shell python -c 'import sys; print "{0}.{1}".format(*sys.version_info[:2])'}
virtualPythonDir   := bla
virtualPythonBinDir := ${shell python -c 'import sys; print "${virtualPythonDir}/" + ("Scripts" if sys.platform == "win32" else "bin")'}

all: docs tests

doc docs:
	make -C Documentation clean html

test tests:
	make -C Tests all

egg: setup.py
	python setup.py --quiet bdist_egg

test_dist:
	rm -fr ${virtualPythonDir}
	virtualenv --no-site-packages --quiet ${virtualPythonDir}
	make egg
	${virtualPythonBinDir}/easy_install --quiet dist/PerformanceAnalyst-${version}-py${pythonVersion}.egg
	@echo "*******************************************************************"
	@echo "* Installation succeeded if the next command prints a Python list *"
	@echo "*******************************************************************"
	${virtualPythonBinDir}/python -c "import PerformanceAnalyst; print dir(PerformanceAnalyst)"

dist: egg test_dist doc
	cd Documentation/_build && zip --recurse-paths ../../dist/PerformanceAnalyst-${version}-doc.zip html
	ls -ltr dist/PerformanceAnalyst-${version}-py${pythonVersion}.egg dist/PerformanceAnalyst-${version}-doc.zip

clean:
	make -C Sources $@
	make -C Tests $@
	rm -fr ${virtualPythonDir}
	find Sources -name "*.pyc" | xargs --no-run-if-empty rm -f

