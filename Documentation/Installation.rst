.. _installation:

************
Installation
************
The PerformanceAnalyst is distributed as a source distribution. The `pip command <http://pip.openplans.org>`_ [#pip]_ can be used to install the distribution-file like this:

.. highlight:: bash

::

  pip install --find-links=file://<path> PerformanceAnalyst==<version>

The `find-links` argument is necessary, because pip normally downloads packages from the `Python Package Index <http://pypi.python.org/pypi>`_, and the PerformanceAnalyst is not available there.

path
  This is the *absolute* path name of the directory containing the source distribution.

version
  This is the version of the PerformanceAnalyst you want to install. Supplying a version is optional and only necessary if you want to install a specific version of the PerformanceAnalyst instead of the latest.

Requirements
************
The PerformanceAnalyst code uses two other packages which need to be installed seperately, depending on the platform:

Matplotlib
  http://matplotlib.sourceforge.net
psutil
  http://code.google.com/p/psutil

************
Uninstalling
************
The PerformanceAnalyst can be uninstalled like this:

.. highlight:: bash

::

  pip uninstall PerformanceAnalyst

.. rubric:: Footnotes

.. [#pip] Pip can be installed like this

   ::

      easy_install pip


