#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="autohockey",
      py_modules=['autohockey'],
      version="0.1",
      description="A simple script to upload a given app to hockeyapp.",
      license="MIT",
      author="Nephila",
      author_email="stagi.andrea@gmail.com",
      url="https://github.com/atooma/autoflight",
      keywords= "hockeyapp ci app ios android test apk ipa script",
      install_requires=[
        "requests",
      ],
      entry_points = {
        'console_scripts': [
            'autohockey = autohockey:main',
        ],
      },
      zip_safe = True)
