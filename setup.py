from distutils.core import setup


setup(
    name = "performance_analyst",
    version = "0.0.9",
    package_dir = {"": "source"},
    packages = ["performance_analyst"],
    scripts=["source/tool/pa.py"],
    author = "Kor de Jong",
    author_email = "info@pcraster.eu",
    description =
        "Software for measuring the performance of snippets of Python code "
        "and storing the results in a database for postprocessing.",
    long_description = file("README.md").read(),
    license = "LICENSE.txt",
    url = "https://github.com/pcraster/performance_analyst",
)
