#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(name="hwt",
      version="3.8",
      description="A library for a construction and analysis of digital circuits",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Nic30/hwt",
      author="Michal Orsak",
      author_email="Nic30original@gmail.com",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: System :: Hardware",
        "Topic :: System :: Emulators",
        "Topic :: Utilities"],
      install_requires=[
          "natsort>=8.4.0",  # natural sorting for HDL objects with name
          "hdlConvertorAst>=1.0", # conversions to SystemVerilog, VHDL
          "ipCorePackager>=0.6",  # generator of IPcore packages (IP-xact, ...)
          "hwtSimApi>=1.3",  # simulator API
          "pyDigitalWaveTools>=1.1",  # simulator output dump
      ],
      license="MIT",
      packages=find_packages(),
      zip_safe=True
)
