from distutils.core import setup

setup(
  name = "PerformanceAnalyst",
  version = "0.0.8",
  package_dir = {"": "Sources"},
  packages = ["PerformanceAnalyst"],
  scripts=["Sources/Tools/pa.py"],
  author = "Kor de Jong",
  author_email = "kdejong@geo.uu.nl",
  description =
    "Software for measuring the performance of snippets of Python code and "
    "storing the results in a database for postprocessing.",
  long_description = file("README.txt").read(),
  license = "LICENSE.txt",
  url = "http://pcraster.sourceforge.net",
)

