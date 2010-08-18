# http://nightly.ziade.org/distribute_setup.py
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
  install_requires=["psutil>=0.1.3"],
  name = "PerformanceAnalyst",
  version = "0.0.2",
  package_dir = {"": "Sources"},
  packages = find_packages(where="Sources"),
  # author = "Kor de Jong",
  # author_email = "kdejong@geo.uu.nl",
  # description = "Dal Python Extension",
  # long_description = "Data abstraction layer for environmental modelling data.",
  # license = "GPL",
  # keywords = ["pcraster environmental modelling data format"],
  # url = "http://pcraster.sourceforge.net",
  zip_safe = True,
)

