#!/usr/bin/env python3

from setuptools import setup

setup(
    name="mpo",
    version="0.1",
    packages=["mpo"],
    license="MIT",
    description="Massively Parallel Optimizations with PyMoo and Dask",
    long_description=open("README.md").read(),
    python_requires=">3.7",
    # do not list standard packages
    install_requires=[
        "pymoo",
        "dask[all]",
        "pydantic",
        "numpy",
        "opencv-python",
    ],
    entry_points={"console_scripts": ["mpo = mpo.__main__:run"]},
)
