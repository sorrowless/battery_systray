#!/usr/bin/env python
from setuptools import setup
import glob
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
  long_description = f.read()

setup(name='batticon',
      version='0.1.2',

      author="Stanislaw Bogatkin",
      author_email="sbog@sbog.ru",

      description="This is a simple battery indicator for system tray",
      long_description=long_description,
      url='https://github.com/sorrowless/battery_systray',
      keywords="battery indicator systray system tray",
      license="GPL",

      packages=['batticon'],

      data_files=[('/usr/share/batticon/themes/baloon', glob.glob('batticon/themes/baloon/*')),
                  ('/usr/share/batticon/themes/faenza', glob.glob('batticon/themes/faenza/*')),
                  ('/usr/share/batticon/themes/minimalbatt', glob.glob('batticon/themes/minimalbatt/*')),
                  ('/usr/share/batticon/themes/monochrome_blch', glob.glob('batticon/themes/monochrome_blch/*')),
                  ('/usr/share/batticon/themes/monochrome_grch', glob.glob('batticon/themes/monochrome_grch/*')),
                  ('/usr/share/batticon/themes/mono-dark', glob.glob('batticon/themes/mono-dark/*')),
                  ('/usr/share/batticon/themes/mono-light', glob.glob('batticon/themes/mono-light/*')),
                  ('/usr/share/batticon/themes/numbers', glob.glob('batticon/themes/numbers/*')),
                  ('/usr/share/batticon/themes/rafeviper', glob.glob('batticon/themes/rafeviper/*')),
                  ('/usr/share/batticon/themes/simplewhite', glob.glob('batticon/themes/simplewhite/*')),
                  ('/usr/share/batticon/themes/superminimal', glob.glob('batticon/themes/superminimal/*')),
                  ('/usr/share/batticon/themes/token', glob.glob('batticon/themes/token/*')),
                  ('/etc/batticon', ['batticon/settings.json'])
                ],

      entry_points={
        'console_scripts': [
          'batticon=batticon.batticon:main',
        ],
      },
)
