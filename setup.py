from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='elistc-nsga-2',
    version='1.3.0',
    description='A NSGA-II implementation using binary chromosome',
    long_description='A NSGA-II implementation',
    url='https://github.com/sayan1886/Elistic-NSGA-II',
    author='Sayan Chatterjee',
    author_email='sayan1886@gmail.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    keywords='nsga2 nsga ga multi-objective',
    license='MIT',
    install_requires=['tqdm'],
)
