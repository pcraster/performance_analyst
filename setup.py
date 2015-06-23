import sys
# from distutils.core import setup
from setuptools import setup
sys.path = ["source"] + sys.path
import performance_analyst as pa


setup(
    name = "performance_analyst",
    version = pa.version_as_string(),
    description =
        "Software for measuring the performance of snippets of Python code "
        "and storing the results in a database for postprocessing.",
    long_description = file("README.md").read(),
    url = "https://github.com/pcraster/performance_analyst",
    author = "PCRaster R&D Team",
    author_email = "info@pcraster.eu",
    license = "LICENSE.txt",
    package_dir = {"": "source"},
    packages = ["performance_analyst"],
    install_requires=["matplotlib", "psutil"],
    scripts=["source/tool/pa.py"],
)
