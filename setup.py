#!/usr/bin/env python
from setuptools import setup
import glob

themes_files = glob.glob('batticon','themes','*')

setup(name='battery-systray',
      version='0.1.0',
      author="Stanislaw Bogatkin",
      author_email="sbog@sbog.ru",
      description="This is a simple battery incdicator for system tray",
      keywords="battery indicator systray system tray",
      licence="GPL",

      packages=['batticon'],
      )
