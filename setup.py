#!/usr/bin/env python
"""
txosc installation script
"""
from setuptools import setup
import os
import sys
import subprocess
import openshow
from twisted.python import procutils

setup(
    name = "openshow",
    version = openshow.__version__,
    author = "Alexandre Quessy, Sofian Audry, Dame Diongue",
    author_email = "alexandre@quessy.net",
    url = "http://github.com/mapmapteam/openshow",
    description = "Open Show Control",
    scripts = [
        "scripts/openshow", 
        ],
    license="LGPL",
    packages = ["openshow", "openshow/test"],
    long_description = """OpenShow is a show control app to trigger theatrical cues at a specific time..""",
    classifiers = [
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
        ]
    )

if sys.argv[1] == "build":
    commands = [
        'help2man --no-info --include=man-openshow.txt --no-discard-stderr --name="OpenShow" ./scripts/openshow --output=openshow.1',
        ]
    if os.path.exists("man-openshow.txt"):
        try:
            help2man = procutils.which("help2man")[0]
        except IndexError:
            print("Cannot build the man pages. help2man was not found.")
        else:
            for c in commands:
                print("$ %s" % (c))
                retcode = subprocess.call(c, shell=True)
                print("The help2man command returned %s" % (retcode))
