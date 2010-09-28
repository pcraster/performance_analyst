version := 0.0.5

all: docs tests

doc docs:
	make -C Documentation clean html

test tests:
	make -C Tests all

egg: setup.py
	python setup.py --quiet bdist_egg

test_dist:
	rm -fr bla
	virtualenv --no-site-packages --quiet bla
	make egg
	bla/bin/easy_install --quiet dist/PerformanceAnalyst-${version}-py?.?.egg
	@echo "*******************************************************************"
	@echo "* Installation succeeded if the next command prints a Python list *"
	@echo "*******************************************************************"
	bla/bin/python -c "import PerformanceAnalyst; print dir(PerformanceAnalyst)"

dist: egg test_dist doc
	cd Documentation/_build && zip --recurse-paths ../../dist/PerformanceAnalyst-${version}-doc.zip html
	ls -ltr dist/PerformanceAnalyst-${version}-py?.?.egg dist/PerformanceAnalyst-${version}-doc.zip

clean:
	make -C Sources $@
	make -C Tests $@
	rm -fr bla
	find Sources -name "*.pyc" | xargs --no-run-if-empty rm -f

