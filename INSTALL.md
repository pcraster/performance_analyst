# Installation
The Performance Analyst is distributed as a so called *wheel* file. The
[pip command](http://pip.openplans.org) can be used to install the
distribution-file like this:

```bash
pip install --find-links=file://<path> performance_analyst==<version>
```

**path**: This is the *absolute* path name of the directory containing
the source distribution.

**version**: This is the version of the Performance Analyst you want
to install. Supplying a version is optional and only necessary if you
want to install a specific version of the Performance Analyst instead of
the latest.

The `--find-links` argument is necessary, because pip normally downloads
packages from the [Python Package Index](http://pypi.python.org/pypi),
and the Performance Analyst is not available there.

During the installation, some additional dependencies may be downloaded
from the Python Package Index, depending on whether or not they are
already installed.

Pip doesn't understand Windows share names, so you need to copy the
distribution file to your local computer if it is located on a share.

Cygwin users using a Windows version of Python (instead of the one that
is packed with Cygwin) can use the folowing command to install a source
distribution file located in the current directory:

```bash
pip install --find-links=file://`cygpath -w \`pwd\`` performance_analyst
```


## Requirements
The Performance Analyst code makes use of other packages. Unless they
are already installed, pip will download these when the Performance
Analyst is installed.

- Matplotlib: http://matplotlib.sourceforge.net
- Numpy: http://www.numpy.org
- psutil: https://github.com/giampaolo/psutil


## Uninstalling
The Performance Analyst can be uninstalled like this:

```bash
pip uninstall performance_analyst
```
