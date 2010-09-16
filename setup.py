# http://nightly.ziade.org/distribute_setup.py
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
  # install_requires=["psutil>=0.1.3"], And matplotlib. Doesn't work on Windows.
  name = "PerformanceAnalyst",
  version = "0.0.5",
  package_dir = {"": "Sources"},
  packages = find_packages(where="Sources"),
  # package_data = {"": ["Documentation/_build/html/*"]},
  scripts=["Sources/Tools/pa.py"],
  author = "Kor de Jong",
  author_email = "kdejong@geo.uu.nl",
  # description = "xxx",
  # long_description = "xxx",
  license = "MIT, http://www.opensource.org/licenses/mit-license.html",
  # keywords = ["xxx xxx xxx"],
  url = "http://pcraster.sourceforge.net",
  zip_safe = True,
)

