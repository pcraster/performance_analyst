from distutils.core import setup


setup(
    name = "PerformanceAnalyst",
    version = "0.0.9",
    package_dir = {"": "source"},
    packages = ["PerformanceAnalyst"],
    scripts=["source/tool/pa.py"],
    author = "Kor de Jong",
    author_email = "kdejong1@uu.nl",
    description =
        "Software for measuring the performance of snippets of Python code "
        "and storing the results in a database for postprocessing.",
    long_description = file("README.rst").read(),
    license = "LICENSE.txt",
    url = "https://github.com/pcraster/performance_analyst",
)
