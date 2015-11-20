from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='todoist-na-plugin',

    version='0.0.1',

    description='Plugin for next action labeling',
    long_description=long_description,

    url='git@bitbucket.org:arch_2/todoist-na-plugin.git',

    author='Daniel Szpisjak',
    author_email='felin.arch@gmail.com',

    license='MIT',

    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
      'todoist-python'
    ],

    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },

    entry_points={
        'console_scripts': [
            'todoer=app:main'
        ]
    }
)
