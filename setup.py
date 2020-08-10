from setuptools import setup

requirements = []
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name = "trackrr.py",
    version = "0.0.1",
    author = "ms7m",
    description = "An asynchronous Python API wrapper for Trackrr.",
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    url = "https://github.com/TheRealKeto/Trackrr.py",
    packages = ["trackrr", "trackrr.ext"],
    install_requires = requirements,
    python_requires = ">=3.5.3"
)
