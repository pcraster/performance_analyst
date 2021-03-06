version := 0.0.13
python_version := ${shell python -c 'import sys; print "{0}.{1}".format(*sys.version_info[:2])'}
virtual_python_dir := bla
virtual_python_bin_dir := ${shell python -c 'import sys; print "${virtual_python_dir}/" + ("Scripts" if sys.platform == "win32" else "bin")'}

all: docs tests

doc docs:
	make -C documentation clean html

test tests:
	make -C test all

# Open all files containing the version number.
bump_version:
	vi Makefile documentation/conf.py CHANGES.md source/tool/pa.py source/performance_analyst/configuration.py

# Create performance_analyst-<version>.{tar.gz,zip}
sdist: setup.py
	python setup.py --quiet sdist --formats=gztar,zip

wheel: setup.py
	python setup.py --quiet bdist_wheel

dist: docs wheel
	cd documentation/_build && zip --quiet --recurse-paths ../../dist/performance_analyst-${version}-doc.zip html
	ls -ltr dist/performance_analyst-${version}*

# Install the package in a sandbox and import it.
test_dist: dist
	rm -fr ${virtual_python_dir}
	virtualenv --no-site-packages --quiet ${virtual_python_dir}
	make wheel
	PYTHONPATH="" ${virtual_python_bin_dir}/pip install --find-links=dist performance_analyst
	@echo "*******************************************************************"
	@echo "* Installation succeeded if the next command prints a Python list *"
	@echo "* and the output of pa.py plot --help                             *"
	@echo "*******************************************************************"
	PYTHONPATH="" ${virtual_python_bin_dir}/python -c "import performance_analyst; print dir(performance_analyst)"
	PYTHONPATH="" ${virtual_python_bin_dir}/pa.py plot --help

clean:
	make -C source $@
	make -C test $@
	rm -fr ${virtual_python_dir}
	find source -name "*.pyc" | xargs --no-run-if-empty rm -f
