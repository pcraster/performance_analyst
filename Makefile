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
	bla/bin/easy_install --quiet dist/PerformanceAnalyst-?.?.?-py?.?.egg
	@echo "*******************************************************************"
	@echo "* Installation succeeded if the next command prints a Python list *"
	@echo "*******************************************************************"
	bla/bin/python -c "import psutil, PerformanceAnalyst; print dir(PerformanceAnalyst)"

dist: egg test_dist doc
	zip --recurse-paths --junk-paths PerformanceAnalyst.zip Documentation/_build/html
	ls -ltr dist/PerformanceAnalyst-*.egg PerformanceAnalyst.zip

clean:
	make -C Sources $@
	make -C Tests $@
	rm -fr bla
	find Sources -name "*.pyc" | xargs --no-run-if-empty rm -f

# 	make -C Documentation $@
# 	rm -fr build dist MANIFEST

