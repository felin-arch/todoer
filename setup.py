from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='todoer',

    version='0.0.1',

    description='Plugin for todoist',
    long_description=long_description,

    url='git@bitbucket.org:arch_2/todoist-na-plugin.git',

    author='Daniel Szpisjak',
    author_email='felin.arch@gmail.com',

    license='MIT',

    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    include_package_data=True,

    install_requires=[
        'todoist-python',
        'ruamel.yaml'
    ],

    extras_require={
        'dev': ['nose2', 'pep8', 'autopep8'],
        'test': [],
    },

    entry_points={
        'console_scripts': [
            'todoer=app:main'
        ]
    }
)
